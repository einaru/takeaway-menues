# -*- coding: utf-8 -*-
"""
Copyright (C) 2011 Einar Uvsløkk <einar.uvslokk@linux.com>.

Free use of this software is granted under the terms of the Do What The
Fuck You Want To Public License, Version 2, as publised by Sam Hocevar.
See http://sam.zoy.org/wtfpl/COPYING for more details.
"""
import os
import shutil
import sys
from glob import glob
from distutils.core import setup

from src import info


def fullSplit(path, result=None):
    """Split a pathname into components (the opposite of os.path.join)
    in a platform-neutral way.
    """
    if result is None:
        result = []

    head, tail = os.path.split(path)

    if head == '':
        return [tail] + result

    if head == path:
        return result

    return fullSplit(head, [tail] + result)


def findPackages():
    """Custom method to suplement distutils with a setuptools-like way
    of finding all package files
    """
    skipDirs = ['rejects', 'test']
    packages = []
    root_dir = os.path.dirname(__file__)
    if root_dir != '':
        os.chdir(root_dir)

    for path, names, files in os.walk(src_dir):
        top = os.path.split(path)[1]
        # Skip directories defined in `skipDirs`
        if top in skipDirs:
            continue

        for i, name in enumerate(names):
            if name.startswith('.'):
                del names[i]

        if '__init__.py' in files:
            s = fullSplit(path)
            if s[0] == src_dir:
                s[0] = app_dir

            packages.append('.'.join(s))

    return packages


# Some default values shared among platforms
src_dir = 'src'
app_dir = 'takeaway'
_author = 'Einar Uvsløkk'
_author_email = 'einar.uvslokk@linux.com'
_url=''
_data_files = []
textfiles = [
    'COPYING',
    'README',
]
# For a complete list of available classifiers, see:
# http://pypi.python.org/pypi?%3Aaction=list_classifiers
_classifiers = [
    'Development Status :: 1 - Alpha',
    'License :: OSI Approved',
    'Topic :: Utilities',
]
_extras = dict()


if __name__ == '__main__':

    success = setup(
        name = info.NAME,
        version = info.VERSION,
        author=_author,
        author_email=_author_email,
        url=_url,
        description=info.DESCRIPTION,
        license='Do What The Fuck You Want Public License, Version 2',
        packages=findPackages(),
        package_dir={
            app_dir: src_dir,
        },
        classifiers=_classifiers,
        **_extras
    )


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
