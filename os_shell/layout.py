#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.layout.controls import BufferControl, FillControl
from prompt_toolkit.token import Token
from prompt_toolkit.shortcuts import create_prompt_layout
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.buffer import AcceptAction
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from os_shell.lexer import OSLexer
from os_shell.toolbar import Toolbar
from os_shell.resources import Resource
from os_shell.completer import OSCompleter
from os_shell.os_commandhelper import OSCommandHelper


class OSBuffer(object):
    def __init__(self):
        history = InMemoryHistory()
        os_commandhelper = OSCommandHelper()
        resource = Resource()
        os_completer = OSCompleter(os_commandhelper, resource)

        self.main_buffer = Buffer(
            accept_action=AcceptAction.RETURN_DOCUMENT,
            history=history,
            auto_suggest=AutoSuggestFromHistory(),
            completer=os_completer,
            complete_while_typing=True)

        self.help_buffer = Buffer(
            is_multiline=True)
        self.help_buffer.text = "HELP"

        os_completer.help_buffer = self.help_buffer

        self.buffers = {
            DEFAULT_BUFFER: self.main_buffer,
            'HELP': self.help_buffer
        }



class OSLayout(object):
    def __init__(self,
                 message="openstack> ",
                 menu_height=12,
                 multiwindow=False):
        toolbar = Toolbar()
        main_layout = create_prompt_layout(
             message=message,
             lexer=OSLexer,
             get_bottom_toolbar_tokens=toolbar.handler,
             reserve_space_for_menu=menu_height)

        if multiwindow:
            self.mlayout = VSplit([
                main_layout,
                Window(width=D.exact(1),
                       content=FillControl('|', token=Token.Line)),
                Window(width=D.exact(70),
                       wrap_lines=True,
                       content=BufferControl(buffer_name='HELP')),
            ])

        if multiwindow:
            self.layout = self.mlayout
        else:
            self.layout = main_layout


    def get_layout(self):
        return self.layout

