from __future__ import absolute_import, unicode_literals


class Tree(object):
    def __init__(self, element):
        """
        :param element: lxml.etree._Element
        """
        self._string = element.get('string')
        self._infinite = element.get('infinite', None)
        self._colors = element.get('colors', None)
        self._status = element.get('status', None)
        self._editable = element.get('editable', None)
        self._element = element


    @property
    def string(self):
        return self._string

    @property
    def infinite(self):
        return self._infinite

    @property
    def fields(self):
        for field in self._element.xpath('field'):
            pass
