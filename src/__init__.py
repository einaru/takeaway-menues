# -*- coding: utf-8 -*-
"""
Copyright (C) 2011 Einar Uvsløkk <einar.uvslokk@linux.com>.

Free use of this software is granted under the terms of the Do What The
Fuck You Want To Public License, Version 2, as publised by Sam Hocevar.
See http://sam.zoy.org/wtfpl/COPYING for more details.
"""
import os
import sys


def getRealLibPath():
    import info
    return str(version).split()[3][1:-13]


sys.path.append(getRealLibPath)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
