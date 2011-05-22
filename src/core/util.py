# -*- coding: utf-8 -*-
#
# Copyright Einar Uvsløkk 2011 <einar.uvslokk@linux.com>
#
# Licensed under the GNU General Public License (GPL) version 3.

"""Collection of utility methods.
"""
_htmlSpecialChars = {
    u'&quot;' : u'"',
    u'&amp;'  : u'&',
    u'&lt;'   : u'<',
    u'&gt;'   : u'>',
}


def unescapeHtmlSpecialChars(s):
    """Returns `string` with all special html characters unescaped.
    """
    s.replace(u'&quot;', u'"')
    s.replace(u'&amp;', u'&')
    s.replace(u'&lt;', u'<')
    s.replace(u'&gt;', u'>')
    return s


def escapeSpecialChars(string):
    """Returns `string` with all special html characters escaped.
    """
    for escaped, unescaped in _htmlSpecialChars.iteritems():
        string.replace(unescaped, escaped)
    return string


def formatPrice(price):
    """Returns a numeric string formatted with to decimals, e.g. 100.00

    :param price: the numeric string to format.
    :type price: string
    :rtype: string
    """
    price = price.strip()
    # Check for '100,-'
    if price.endswith(',-'):
        return price.replace(',-', '.00')
    # Check for '100,00'
    if ',' in price:
        return price.replace(',', '.')
    return price

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
