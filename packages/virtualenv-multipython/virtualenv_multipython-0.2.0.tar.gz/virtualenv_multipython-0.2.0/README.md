# virtualenv-multipython
> virtualenv discovery plugin for [multipython](https://github.com/makukha/multipython).

[![license](https://img.shields.io/github/license/makukha/virtualenv-multipython.svg)](https://github.com/makukha/virtualenv-multipython/blob/main/LICENSE)
[![versions](https://img.shields.io/pypi/pyversions/virtualenv-multipython.svg)](https://pypi.org/project/virtualenv-multipython)
[![pypi](https://img.shields.io/pypi/v/virtualenv-multipython.svg#v0.2.0)](https://pypi.python.org/pypi/virtualenv-multipython)

> [!NOTE]
> * [virtualenv-multipython]() has twin plugin [tox-multipython](https://github.com/makukha/tox-multipython) that serves the same purpose for tox v3 and `python<3.7`.

This [virtualenv](https://virtualenv.pypa.io) plugin comes pre-installed in [multipython](https://hub.docker.com/r/makukha/multipython) Docker image and is responsible for resolving tox environment name to Python executable. Most probably, you don't need to install it yourself.

Its purpose is to support resolution of environment names equal to multipython tags. In particular, they include free threading Python builds `py313t` and `py314t`.

| tox env | Executable   |
|---------|--------------|
| `pyXY`  | `pythonX.Y`  |
| `pyXYt` | `pythonX.Yt` |

Other patterns are passed to built-in virtualenv discovery.

More env names may be added in the future.

> [!IMPORTANT]
> * This plugin does not fall back to tox python: interpreter discovery errors are explicit.

# Testing

`virtualenv-multipython` is tested for all Python tags supported by [multipython](https://github.com/makukha/multipython), except `py{27,35,36}` as not matching project requirements. See `tests/docker-bake.hcl` for details.

# Authors

* [Michael Makukha](https://github.com/makukha)

This package is a part of [multipython](https://github.com/makukha/multipython) project.


## License

[MIT License](https://github.com/makukha/caseutil/blob/main/LICENSE)
