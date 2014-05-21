#!/usr/bin/env python

#from setuputils import setup
from distutils.core import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt")

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

sctk = {
    "name": "sctk",
    "description": "scad tool kit",
    "author":"Giles Hall",
    "packages": ["sctk"],
    "package_dir": {"sctk": "src"},
    'py_modules':['sctk.__init__', 'sctk.api', 'sctk.utils'],
    "version": "1.0",
    #"install_requires": reqs,
}

if __name__ == "__main__":
    setup(**sctk)