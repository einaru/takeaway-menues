# -*- coding: utf-8 -*-
"""
Copyright (C) 2011 Einar Uvsløkk, <einar.uvslokk@linux.com>.

Free use of this software is granted under the terms of the Do What The
Fuck You Want To Public License, Version 2, as publised by Sam Hocevar.
See http://sam.zoy.org/wtfpl/COPYING for more details.


This module contains specialized `Restaurant` classes for scraping
takeout menu information from their websites.

Currently `Restaurant` implementations exists for:

- Kyoto Sushi | Vin & Cocktailbar (Trondheim)
- Bryggen Asian Cooking (Trondheim)

Not currently implemented:

- Sushi Bar    (Trondheim) http://www.sushibar.no **pdf**
- Phu Yen      (Trondheim) http://www.phuyen.no   **Flash, pdf**
- Sesam Burger (Trondheim)                        **No website**
"""
import re
import sys
import urllib2
from urlparse import urlparse, urlunparse

from BeautifulSoup import BeautifulSoup, SoupStrainer

from menu import (Menu, MenuItem)
import util


class Restaurant(object):
    """Abstract class representing a restaurant."""

    def __init__(self, name, url=''):
        """
        :param name: The name of the restaturant.
        :type name: string
        :param url: The webiste url for the restaturant.
        :type url: string
        :param menu: The `Menu` object for the restaurant.
        :type menu: `Menu`
        """
        self.name = name
        self.url = url
        self.menu = Menu()

    def prettify(self, out=sys.stdout):
        """Writes the menu to stdout, in a pretty format."""

        print >> out, self.name
        print >> out, '=' * len(self.name)
        print >> out, self.url
        print >> out

        for section, items in self.menu.getMenu().iteritems():
            print >> out, section.encode('utf-8')
            print >> out, '-' * 79
            for i, item in enumerate(items):
                print >> out, ' %2d %s' % (i + 1, item.name.encode('utf-8')),
                width = 73 - len(item.name)
                print >> out, '%s' % (item.price.rjust(width))
            print >> out


class Kyoto(Restaurant):
    """Class representing Kyoto Sushi in Trondheim."""

    def __init__(self):
        super(Kyoto, self).__init__(
            'Kyoto',
            'http://www.kyoto.no/take-away/'
        )

    def scrape(self):
        """Scrape the takeout menu off `Kyoto.url`.

        First finds all submenu takeout menues with `_getSubmenuUrls`,
        and then uses `_processSubmenu` to process each submenu.

        The submenus will be stored in `Kyoto.menu`.
        """
        submenues = self._getSubmenuUrls()
        for url in submenues:
            html = urllib2.urlopen(url).read()
            soup = BeautifulSoup(html, convertEntities='html')

            # Retrive the section name
            info = soup.find('div', 'blank')
            section = info.h1.contents[0].split('/')[0].strip()

            submenu = self._processSubmenu(soup)
            self.menu.addSubmenu(submenu, section)

    def _getSubmenuUrls(self):
        """Returns all submenu urls off `Kyoto.url`."""
        html = urllib2.urlopen(self.url).read()
        urls = ''.join(re.findall('<a href="take-away_.+?">', html))
        # Parsing the url to get components to the netloc
        o = urlparse(self.url)
        # Unparse the url components to get the base url with suffix `/`
        u = urlunparse((o.scheme, o.netloc, '/', '', '', ''))
        return ['%s%s' % (u, a['href']) for a in BeautifulSoup(urls)]

    def _processSubmenu(self, soup):
        """Scrapes a Kyoto submenu.

        Html structure for takeout (sub)menu::

            <table class="menytabell">
              <tbody>
                <tr>
                  <td class="menyinfo">Item info</td>
                  <td class="menypris">Item price</td>
                </tr>
                ...
              </tbody>
            </table>

        :param soup: the BeautifulSoup object holding a Kyoto submenu
         page.
        :type soup: `BeautifulSoup`
        """
        items = []
        table = soup.find('table', 'menytabell')
        for row in table.findAll('tr'):
            info = row.find('td', 'menyinfo')
            name, desc = self._processMenuinfo(info)
            price = row.find('td', 'menypris').contents[0]
            price = util.formatPrice(price)

            items.append(MenuItem(name, desc, price))

        return items

    def _processMenuinfo(self, info):
        """Returns a tuple (name, desc) for the menyinfo class item.

        Regarding the the menyinfo class, the contents can occure in
        multiple ways:

        1. ['Name/en_US']
        2. ['Name', <em>en_US</em>]
        3. ['Name, <br />, <em>en_US</em>]
        4. ['\n', <p>Name</p>, '\n', <p>Info<br /><em>en_US</em></p>, '\n']
        5. ['\n', '<p>Name</p>, '\n', <p><em>en_US</em></p>, '\n']

        :param info: the `BeautifulSoup` object holding menu item info.
        :type info: `BeautifulSoup`
        :rtype: tuple
        """
        name = ''
        #: Norwegian desc.
        nb_NO = ''
        #: English desc.
        en_US = ''
        #: The lenght is used to determine the different cases.
        _len = len(info.contents)

        # Case 1.
        if _len == 1:
            name, en_US = info.contents[0].split('/')

        # Case 2. and 3.
        if _len == 2 or _len == 3:
            name = info.contents[0]
            try:
                en_US = info.em.contents[0]
            except IndexError:
                pass

        # Case 4. and 5.
        if _len == 5:
            p = info.findAll('p')
            name = p[0].contents[0]
            nb_NO = p[1].contents[0]
            en_US = p[1].em.contents[0]

        # FIXME: As of now the `Menu` DS do not support multiple locales
        # for the item description, and thus the en_US description is
        # not used.
        #return (name, (nb_NO, en_US))
        return (name, nb_NO)


class BryggenAsianCooking(Restaurant):
    """Class representing Bryggen Asian Cooking in Trondheim."""

    def __init__(self):
        super(BryggenAsianCooking, self).__init__(
            'Bryggen Asian Cooking',
            'http://bryggenasiancooking.no/take-away'
        )

    def scrape(self):
        """Specialized screen scraping for Bryggen Asiancooking.

        Html structure for takeout menu::

            ...
            <form>
                <h2>Menu section name 1</h2>
                <p>Possible menu section description</p>
                <table>
                    ...
                </table>
                <h2>Menu section name 2</h2>
                ...
            </form>
            ...
        """
        html = urllib2.urlopen(self.url).read()
        soup = BeautifulSoup(html, convertEntities='html')
        #: this contains all the menu info as regular html
        form = soup.form
        for table in form.findAll('table'):
            section = table.findPrevious('h2').contents[0]
            menuitems = self._processSubmenu(table)
            self.menu.addSubmenu(menuitems, section)

    def _processSubmenu(self, soup):
        """Scrape a Bryggen Asian Cooking submenu.

        Each submenu is inside a table:

            <table>
                <tr>
                    <td>Menu item name<br/>possible description</td>
                    <td>Menu item price</td>
                    <td>IGNORE</td>
                </tr>
                ...
            </table>

        :param soup: the `BeautifulSoup` object holding submenu data.
        :type soup: `BeautifulSoup`
        :rtype: list of `MenuItem`
        """
        items = []
        for row in soup.findAll('tr'):
            td = row.findAll('td', limit=2)
            info = td[0].contents
            name = info[0]
            if len(info) > 1:
                desc = info[2].encode('utf-8').strip('\n')
            else:
                desc = u''
            price = util.formatPrice(td[1].contents[0])

            items.append(MenuItem(name, desc, price))

        return items


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
