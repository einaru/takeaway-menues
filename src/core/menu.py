# -*- coding: utf-8 -*-
#
# Copyright Einar Uvsløkk 2011 <einar.uvslokk@linux.com>
#
# Licensed under the GNU General Public License (GPL) version 3.

"""This module contains methods for accessing menues from the various
supported restaturants.
"""


class Menu(object):
    """Represents a menu from a restaturant.

    Contains the name of the restaurant, and a list of `MenuItem` for
    this restaturants menu::

        {
            ...
            section: [`MenuItem`, `MenuItem`, ...],
            ...
        }
    """
    def __init__(self, menu={}):
        self._menu = menu

    def addItem(self, item, section='default'):
        """Add a single menu item to the menu.

        :param items: the list of menu items to add to this menu.
        :type items: list of `MenuItem`
        :param section: Optional section name for the menu items.
        :type section: string
        """
        if section in self._menu:
            self._menu[section].append(item)
        else:
            self._menu[section] = [item]

    def addSubmenu(self, submenu, section):
        """Add a complete `submenu` to `section` in the menu.

        Note that if the `section` exists, the `submenu` will be
        extended to the present submenu.

        :param submenu: the submenu to add to the menu.
        :type submenu: list of `MenuItem`
        :param section: the menu section to add the submenu to.
        :type section: string
        """
        if section in self._menu:
            self._menu[section].extend(submenu)
        else:
            self._menu[section] = submenu

    def getMenu(self, section=None):
        """Returns the ds for the menu. If `section` is provided the
        submenu is returned, if the `section` is invalid ``None`` is
        returned.

        :param section: optional section to get a submenu.
        :type section: string
        """
        if section is None:
            return self._menu

        if section in self._menu:
            return self._menu[section]

        return None


class MenuItem(object):
    """Represents an item in a menu."""

    def __init__(self, name='', desc='', price=0):
        """
        :param name: the name of the menu item.
        :type name: string
        :param desc: a description for the menu item.
        :type desc: string
        :param price: the price for the menu item.
        :type price: int
        """
        self.name = name
        self.desc = desc
        self.price = price

    def __str__(self):
        return 'name: %s\ndesc: %s\nprice: %s' % (self.name, self.desc, self.price)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
