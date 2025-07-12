import pluggy
import importlib
import sys
from functools import lru_cache
from runpy import run_module

from .hookspecs import vidtoolzSpec

DEFAULT_PLUGINS = ("vidtoolz.default_plugins.reverse",)

pm = pluggy.PluginManager("vidtoolz")
pm.add_hookspecs(vidtoolzSpec)


@lru_cache(maxsize=1)
def load_plugins():
    """Load plugins only once using lru_cache instead of a global flag."""
    if not getattr(sys, "_called_from_test", False):
        pm.load_setuptools_entrypoints("vidtoolz_plugins")
        for plugin in DEFAULT_PLUGINS:
            try:
                mod = importlib.import_module(plugin)
                pm.register(mod, plugin)
            except ImportError as e:
                print(f"[Plugin Load Error] Could not load {plugin}: {e}")


def get_plugins(args=None):
    plugins = []
    if not getattr(sys, "_called_from_test", False):
        plugin_to_distinfo = dict(pm.list_plugin_distinfo())
        for plugin in pm.get_plugins():
            plugin_info = {
                "name": plugin.__name__,
                "hooks": [h.name for h in pm.get_hookcallers(plugin)],
            }
            distinfo = plugin_to_distinfo.get(plugin)
            if distinfo:
                plugin_info["version"] = distinfo.version
                plugin_info["name"] = distinfo.project_name
            plugins.append(plugin_info)

    if plugins:
        print("Installed Plugins:")
        for p in plugins:
            print(f"- {p['name']} (version: {p.get('version', 'unknown')})")
    else:
        print("No external plugins in environment.")

    return plugins


def install_plugin(
    packages, upgrade=False, editable=None, force_reinstall=False, no_cache_dir=False
):
    """Install packages from PyPI into the same environment as vidtoolz."""
    args = ["pip", "install"]
    if upgrade:
        args.append("--upgrade")
    if editable:
        args += ["--editable", editable]
    if force_reinstall:
        args.append("--force-reinstall")
    if no_cache_dir:
        args.append("--no-cache-dir")
    args += list(packages)

    sys.argv = args
    run_module("pip", run_name="__main__")
