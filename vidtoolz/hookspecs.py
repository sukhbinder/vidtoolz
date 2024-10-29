from pluggy import HookimplMarker
from pluggy import HookspecMarker


hookspec = HookspecMarker("vidtoolz")
hookimpl = HookimplMarker("vidtoolz")


class vidtoolzSpec:
    @hookspec
    def register_commands(subparser):
        """Register additional CLI sub commands, e.g. 'vidtoolz mycommand ...'"""
