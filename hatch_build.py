"""Keep repository ignore files out of the source distribution."""

from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        if self.target_name == "sdist":
            forced = build_data["force_include"]
            for path in list(forced):
                if Path(path).name in {".gitignore", ".hgignore"}:
                    del forced[path]
