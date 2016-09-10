#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
from pygments.token import Token

'''
Toolbar
'''


class Toolbar(object):
    def __init__(self):
        self.handler = self._create_toolbar_handler()

    def _create_toolbar_handler(self):
        def get_toolbar_items(_):
            color_token = Token.Toolbar.On
            color = 'ON'

            fuzzy_token = Token.Toolbar.On
            fuzzy = 'ON'

            shortcuts_token = Token.Toolbar.On
            shortcuts = 'ON'

            #return [
            #    (color_token, ' [F2] Color: {0} '.format(color)),
            #    (fuzzy_token, ' [F3] Fuzzy: {0} '.format(fuzzy)),
            #    (shortcuts_token, ' [F4] Shortcuts: {0} '.format(shortcuts)),
            #    (Token.Toolbar, ' [F5] Refresh '),
            #    (Token.Toolbar, ' [F9] Docs '),
            #    (Token.Toolbar, ' [<C-Q>] Exit ')
            #]

            return [
                (Token.Toolbar, " [Type 'quit' or 'exit'] to Exit ")
            ]

        return get_toolbar_items


