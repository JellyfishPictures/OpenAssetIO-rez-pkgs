# -*- coding: utf-8 -*-

name = 'openassetio'

version = '1.0.0-alpha.3'

requires = [
    'pybind11',
    'catch2',
    'trompeloeil'
]

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python-3.7+']


def commands():
    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
    env.PYTHONPATH.append("{root}/lib/site-packages")


tests = {
    "unit": {
        "command": "pytest tests/python",
        "requires": ["pytest"],
    },
}
