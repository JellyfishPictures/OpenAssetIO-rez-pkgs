# -*- coding: utf-8 -*-

name = 'catch2'

version = '2.13.0'

build_command = "python {root}/rezbuild.py {install}"
build_requires = ['python-3.7+']


def commands():
    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
