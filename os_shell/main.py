#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
from prompt_toolkit import Application, CommandLineInterface, AbortAction
from prompt_toolkit.buffer import AcceptAction
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.shortcuts import create_eventloop, create_prompt_layout


from prompt_toolkit.styles import PygmentsStyle


from completer import OSCompleter
from os_commandhelper import OSCommandHelper
from toolbar import Toolbar
from lexer import OSLexer
from style import OSStyle


OSKeyBinder = KeyBindingManager()


@OSKeyBinder.registry.add_binding(Keys.ControlQ)
def _controlQkey(event):
    '''
    Quit the program when user presses <C-Q>
    '''
    b = event.cli.current_buffer
    b.insert_text(event.data)
    text = b.document.text
    print "text: ", text
    print event


def run():
    history = InMemoryHistory()

    os_commandhelper = OSCommandHelper()
    os_completer = OSCompleter(os_commandhelper)
    toolbar = Toolbar()

    layout = create_prompt_layout(
        message="openstack> ",
        lexer=OSLexer,
        get_bottom_toolbar_tokens=toolbar.handler,
        reserve_space_for_menu=12)

    cli_buffer = Buffer(
        accept_action=AcceptAction.RETURN_DOCUMENT,
        history=history,
        auto_suggest=AutoSuggestFromHistory(),
        completer=os_completer,
        complete_while_typing=True)

    application = Application(
        style=PygmentsStyle(OSStyle),
        layout=layout,
        buffer=cli_buffer,
        on_exit=AbortAction.RAISE_EXCEPTION,
        key_bindings_registry=OSKeyBinder.registry)


    cli = CommandLineInterface(application=application,
                               eventloop=create_eventloop())

    while True:
        document = cli.run(reset_current_buffer=True)
        print "Document: ", document
        process_document(document)


def process_document(document):
    '''
    Process the executed command.
    '''
    # Check for any exit criterias.
    if document.text == "quit" or document.text == "exit":
        print "Exit now!"
        sys.exit()


if __name__ == '__main__':
    run()
