# -*- coding: utf-8 -*-
#
# Copyright Einar Uvsløkk 2011 <einar.uvslokk@linux.com>
#
# Licensed under the GNU General Public License (GPL) version 3.

"""Test module for core.scrapper.py"""

from core.scrapper import *


if __name__ == '__main__':
    """These arguments checks are only for testing."""

    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg.lower().startswith('kyoto'):
            kyoto = Kyoto()
            kyoto.scrape()
            kyoto.prettify()
        elif arg.lower().startswith('bryggen'):
            bryggen = BryggenAsianCooking()
            bryggen.scrape()
            bryggen.prettify()
        sys.exit(0)

    print 'Test usage: %s restaturant' % sys.argv[0]
    sys.exit(1)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
