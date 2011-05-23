# -*- coding: utf-8 -*-
"""
Copyright (C) 2011 Einar Uvsløkk, <einar.uvslokk@linux.com>.

Free use of this software is granted under the terms of the Do What The
Fuck You Want To Public License, Version 2, as publised by Sam Hocevar.
See http://sam.zoy.org/wtfpl/COPYING for more details.


This module contains a collection of utility methods.
"""


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
