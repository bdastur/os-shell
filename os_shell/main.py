#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import os
from prompt_toolkit import Application, CommandLineInterface, AbortAction
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.shortcuts import create_eventloop

from prompt_toolkit.styles import PygmentsStyle

from os_shell.os_commandhelper import OSCommandHelper
from os_shell.style import OSStyle
from os_shell.layout import OSLayout
from os_shell.layout import OSBuffer


OSKeyBinder = KeyBindingManager(enable_search=True,
                                enable_abort_and_exit_bindings=True,
                                enable_system_bindings=True,
                                enable_auto_suggest_bindings=True)


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


@OSKeyBinder.registry.add_binding(Keys.Tab)
def _tabkeyhandler(event):
    '''
    Force autocompletion at cursor
    '''
    pass


def validate_osenvironment():
    '''
    We expect the OS ENV variables to be set when executing.
    '''
    required_env_settings = [
        "OS_USERNAME", "OS_PASSWORD", "OS_AUTH_URL"
    ]

    invalid_settings = []
    for env_setting in required_env_settings:
        if os.environ.get(env_setting, None) is None:
            invalid_settings.append(env_setting)

    if invalid_settings:
        invalid_envstr = " ".join(invalid_settings)
        invalid_envstr += invalid_envstr + " - Not Set"
        print invalid_envstr
        sys.exit()


def print_banner():
    '''
    Print the OS-Shell Banner.
    '''
    banner_str = \
        """
         ____   _____       _____ _          _ _
        / __ \ / ____|     / ____| |        | | |
       | |  | | (___ _____| (___ | |__   ___| | |
       | |  | |\___ \______\___ \| '_ \ / _ \ | |
       | |__| |____) |     ____) | | | |  __/ | |
        \____/|_____/     |_____/|_| |_|\___|_|_|
        """
    print banner_str
    print "An Interactive OpenStack Command Execution Shell.."


def run():
    validate_osenvironment()
    print_banner()

    cli_buffer = OSBuffer()
    ltobj = OSLayout(multiwindow=False)

    application = Application(
        style=PygmentsStyle(OSStyle),
        layout=ltobj.layout,
        buffers=cli_buffer.buffers,
        on_exit=AbortAction.RAISE_EXCEPTION,
        key_bindings_registry=OSKeyBinder.registry)


    cli = CommandLineInterface(application=application,
                               eventloop=create_eventloop())

    while True:
        try:
            document = cli.run(reset_current_buffer=True)
            process_document(document)
        except KeyboardInterrupt:
            # A keyboardInterrupt generated possibly due to Ctrl-C
            print "Keyboard Interrupt Generated"
            continue
        except EOFError:
            print "cntl-D"
            sys.exit()


def process_document(document):
    '''
    Process the executed command.
    '''

    # Check for any exit criterias.
    if document.text == "quit" or document.text == "exit":
        print "Exit now!"
        sys.exit()

    if len(document.text) == 0:
        return

    # Perform our operation.
    cmdlist = document.text.split(" ")
    os_cmdhandler = OSCommandHelper(skip_cache=True)
    os_cmdhandler.execute_openstack_cli(cmdlist)




if __name__ == '__main__':
    run()
