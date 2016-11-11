#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from prompt_toolkit.shortcuts import create_prompt_layout
from os_shell.lexer import OSLexer
from os_shell.toolbar import Toolbar


class OSLayout(object):
    def __init__(self,
                 message="openstack> ",
                 menu_height=12):
        toolbar = Toolbar()
        self.layout = create_prompt_layout(
             message=message,
             lexer=OSLexer,
             get_bottom_toolbar_tokens=toolbar.handler,
             reserve_space_for_menu=menu_height)

    def get_layout(self):
        return self.layout

