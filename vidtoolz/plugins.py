import pluggy
from .hookspecs import vidtoolzSpec
import sys
from runpy import run_module
import importlib

pm = pluggy.PluginManager("vidtoolz")
pm.add_hookspecs(vidtoolzSpec)

DEFAULT_PLUGINS = ("vidtoolz.default_plugins.reverse",)

_loaded = False


def load_plugins():
    global _loaded
    if _loaded:
        return
    _loaded = True
    if not getattr(sys, "_called_from_test", False):
        # Only load plugins if not running tests
        pm.load_setuptools_entrypoints("vidtoolz_plugins")
        for plugin in DEFAULT_PLUGINS:
            mod = importlib.import_module(plugin)
            pm.register(mod, plugin)


def get_plugins(args):
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
            print(p["name"])
    else:
        print("No external plugins in env.")
    return plugins


def install_plugin(packages, upgrade, editable, force_reinstall, no_cache_dir):
    """Install packages from PyPI into the same environment as vidtoolz"""
    args = ["pip", "install"]
    if upgrade:
        args += ["--upgrade"]
    if editable:
        args += ["--editable", editable]
    if force_reinstall:
        args += ["--force-reinstall"]
    if no_cache_dir:
        args += ["--no-cache-dir"]
    args += list(packages)
    sys.argv = args
    run_module("pip", run_name="__main__")
