from pathlib import Path
import re
from typing import TYPE_CHECKING

# ruff: noqa: F401
if TYPE_CHECKING:
    import argparse  # type: ignore[unused-ignore]

from virtualenv.discovery.builtin import Builtin  # type: ignore
from virtualenv.discovery.discover import Discover  # type: ignore
from virtualenv.discovery.py_info import PythonInfo  # type: ignore


MULTIPYTHON_PATH_ROOT = Path('/usr/local/bin')

RX = (
    re.compile(r'(?P<impl>py)(?P<maj>[23])(?P<min>[0-9][0-9]?)'),
    re.compile(r'(?P<impl>py)(?P<maj>3)(?P<min>[0-9][0-9])(?P<suffix>t)'),
)


class Multipython(Discover):  # type: ignore[misc]
    def __init__(self, options):  # type: (argparse.Namespace) -> None
        super().__init__(options)
        self.builtin = Builtin(options)
        self.env = options.env['TOX_ENV_NAME']

    @classmethod
    def add_parser_arguments(cls, parser):  # type: (argparse.ArgumentParser) -> None
        Builtin.add_parser_arguments(parser)

    def run(self):  # type: () -> PythonInfo | None
        match = None
        for rx in RX:
            match = rx.fullmatch(self.env)
            if match is not None:
                break

        if match is None:
            return None

        g = match.groupdict()
        g['suffix'] = g.get('suffix', '')
        name = {'py': 'python'}[g['impl']]
        command = '{name}{maj}.{min}{suffix}'.format(name=name, **g)

        try:
            proposed = PythonInfo.from_exe(
                str(MULTIPYTHON_PATH_ROOT / command),
                resolve_to_host=False,
            )
        except Exception:
            proposed = None

        return proposed
