variable "CASES" {
  default = [
    # NOTE: py20 is always missing in multipython image

    # NOTE: In tests without virtualenv version downpin, py37 should also be failing,
    #   because virtualenv does not support Python 3.7 starting from v20.27.
    #   However, it is still capable to detect 3.7 interpreter, and we use failed tags
    #   list "py20 py27 py35 py36" (without "py37").
    #   One day this test may become broken, and "py37" should be added back.

    { tox_tag = "py314t", venv = "", fail = "py20 py27 py35 py36" },  # be ready to add "py37"
    { tox_tag = "py314t", venv = "<20.27", fail = "py20 py27 py35 py36" },
    { tox_tag = "py314t", venv = "<20.22", fail = "py20" },

    { tox_tag = "py313t", venv = "", fail = "py20 py27 py35 py36" },  # be ready to add "py37"
    { tox_tag = "py313t", venv = "<20.27", fail = "py20 py27 py35 py36" },
    { tox_tag = "py313t", venv = "<20.22", fail = "py20" },

    { tox_tag = "py313", venv = "", fail = "py20 py27 py35 py36" },  # be ready to add "py37"
    { tox_tag = "py313", venv = "<20.27", fail = "py20 py27 py35 py36" },
    { tox_tag = "py313", venv = "<20.22", fail = "py20" },

    { tox_tag = "py312", venv = "", fail = "py20 py27 py35 py36" },  # be ready to add "py37"
    { tox_tag = "py312", venv = "<20.27", fail = "py20 py27 py35 py36" },
    { tox_tag = "py312", venv = "<20.22", fail = "py20" },

    { tox_tag = "py311", venv = "", fail = "py20 py27 py35 py36" },  # be ready to add "py37"
    { tox_tag = "py311", venv = "<20.27", fail = "py20 py27 py35 py36" },
    { tox_tag = "py311", venv = "<20.22", fail = "py20" },

    { tox_tag = "py310", venv = "", fail = "py20 py27 py35 py36" },  # be ready to add "py37"
    { tox_tag = "py310", venv = "<20.27", fail = "py20 py27 py35 py36" },
    { tox_tag = "py310", venv = "<20.22", fail = "py20" },

    { tox_tag = "py39", venv = "", fail = "py20 py27 py35 py36" },  # be ready to add "py37"
    { tox_tag = "py39", venv = "<20.27", fail = "py20 py27 py35 py36" },
    { tox_tag = "py39", venv = "<20.22", fail = "py20" },

    { tox_tag = "py38", venv = "", fail = "py20 py27 py35 py36" },  # be ready to add "py37"
    { tox_tag = "py38", venv = "<20.27", fail = "py20 py27 py35 py36" },
    { tox_tag = "py38", venv = "<20.22", fail = "py20" },

    { tox_tag = "py37", venv = "", fail = "py20 py27 py35 py36" },  # be ready to add "py37"
    { tox_tag = "py37", venv = "<20.27", fail = "py20 py27 py35 py36" },
    { tox_tag = "py37", venv = "<20.22", fail = "py20" },
  ]
}

target "default" {
  dockerfile = "tests/Dockerfile"
  args = {
    TOX_TAG = CASE["tox_tag"],
    VIRTUALENV_PIN = CASE["venv"],
    TAGS_FAILING = CASE["fail"],
  }
  matrix = { CASE = CASES }
  name = "test_${CASE["tox_tag"]}_${regex_replace(CASE["venv"], "[^0-9]", "_")}"
  output = ["type=cacheonly"]
}
