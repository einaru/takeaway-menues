# -*- coding: utf-8 -*-
"""
Copyright (C) 2011 Einar Uvsløkk <einar.uvslokk@linux.com>.

Free use of this software is granted under the terms of the Do What The
Fuck You Want To Public License, Version 2, as publised by Sam Hocevar.
See http://sam.zoy.org/wtfpl/COPYING for more details.
"""
import datetime
import pwd
import os
import optparse
import sys
import urllib2

short_gpl_header = '''# -*- coding: utf-8 -*-
"""
Copyright (C) {0} {1} <{2}>.

Free use of this software is granted under the terms of the
GNU General Public License (GPL) version 3 or later.
"""
'''

short_wtfpl_header = '''# -*- coding: utf-8 -*-
"""
Copyright (C) {0} {1} <{2}>.

Free use of this software is granted under the terms of the Do What The
Fuck You Want To Public License, Version 2, as publised by Sam Hocevar.
See http://sam.zoy.org/wtfpl/COPYING for more details.
"""
'''

short_wtfpl_warranty_header = '''# -*- coding: utf-8 -*-
"""
Copyright (C) {0} {1} <{2}>.

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
"""
'''
long_wtfpl_header = '''# -*- coding: utf-8 -*-
"""
Copyright (C) {0} {1} <{2}>.

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
Version 2, December 2004

Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

0. You just DO WHAT THE FUCK YOU WANT TO.
"""
'''

long_gpl_header = '''# -*- coding: utf-8 -*-
"""
Copyright (C) {0}
    {1} <{2}>

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
'''

vim_footer = """
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4"""


def getCurrentYear():
    return datetime.datetime.now().year


def getHostname():
    return os.uname()[1]


def getUsername():
    return os.getlogin()


def getNameOfUser():
    return pwd.getpwnam(getUsername())[4]


def getBogusEmail():
    return '{0}@{1}'.format(getUsername(), getHostname())


def getLicenseHeader(license, long):
    if license.lower().startswith('wtfpl'):
        if long:
            return long_wtfpl_header
        else:
            return short_wtfpl_header
    if license.lower().startswith('gpl'):
        if long:
            return long_gpl_header
        else:
            return short_gpl_header

    return short_wtfpl_header


#: urls to common open source licenses
LICENSE = {
    'gpl1': 'http://www.gnu.org/licenses/gpl1.txt',
    'gpl2': 'http://www.gnu.org/licenses/gpl2.txt',
    'gpl3': 'http://www.gnu.org/licenses/gpl.txt',
    'lgpl3': 'http://www.gnu.org/licenses/lgpl.txt',
    'wtfpl': 'http://sam.zoy.org/wtfpl/COPYING',
}


def listDownloadableLicenses():
    print >> sys.stdout
    print >> sys.stdout, 'Downloadable licenses:'
    print >> sys.stdout
    for key, value in LICENSE.iteritems():
        print >> sys.stdout, ' ', key
    print >> sys.stdout


def getLicenseCopy(license):
    try:
        html = urllib2.urlopen(LICENSE[license]).read()
        print >> sys.stdout, html
    except KeyError:
        print >> sys.stderr, license, 'is not a valid license identifier.'
        listDownloadableLicenses()
        sys.exit(1)


def main():

    usage = '%prog [-maey]\nTry %prog --help for more information.'

    p = optparse.OptionParser(usage=usage)

    p.add_option(
        '-m', '--module', dest='module',
        action='store', type='string', metavar='MOD',
        help='The name of the program (module, class, etc)'
    )
    p.add_option(
        '-a', '--author', dest='author',
        action='store', type='string', metavar='NAME',
        help='The name of the copyright holder'
    )
    p.add_option(
        '-e', '--email', dest='email',
        action='store', type='string', metavar='EMAIL',
        help='The email address of copyright holder'
    )
    p.add_option(
        '-y', '--year', dest='year',
        action='store', type='string', metavar='YEAR',
        help='The year to insert with the copyright statement.'
    )
    p.add_option(
        '-l', '--license', dest='license',
        action='store', type='string', metavar='LICENSE',
        default='wtfpl',
        help='The LICENSE to use. Defaults to WTFPL.'
    )
    p.add_option(
        '--get', dest='get',
        action='store', type='string', metavar='LICENSE',
        help='Download a copy of LICENSE.'
    )
    p.add_option(
        '--long',
        dest='long', action='store_true',
        help='Generate the long version python header'
    )
    p.add_option(
        '--footer',
        dest='footer', action='store_true',
        help='Generate the vim-macro footer.'
    )

    (opt, arg) = p.parse_args()

    if opt.footer:
        print >> sys.stdout, vim_footer
        sys.exit(0)

    if opt.get:
        getLicenseCopy(opt.get)
        sys.exit(0)

    name = getNameOfUser()
    email = getBogusEmail()
    year = getCurrentYear()
    module = 'This'
    if opt.author:
        name = opt.name

    if opt.email:
        email = opt.email

    if opt.year:
        year = opt.year

    if opt.module:
        module = opt.module

    license = getLicenseHeader(opt.license, opt.long)
    print >> sys.stdout, license.format(year, name, email)


if __name__ == '__main__':
    main()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4'
