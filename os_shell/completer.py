#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prompt_toolkit.completion import Completer, Completion


class OSCompleter(Completer):
    '''
    Our Custom Completer, which is a subclass of the prompt_toolkit
    Completer class.
    '''
    def __init__(self, os_commandhandler):
        self.os_commandhandler = os_commandhandler

    def parse_document(self, document):
        '''
        Return a list of commands from the parsed
        document text.
        '''
        cmdlist = document.text.split(" ")
        for cmd in cmdlist:
            if cmd == "" or cmd == " ":
                cmdlist.remove(cmd)

        return cmdlist

    def get_current_command_options(self, cmdlist):
        '''
        The function will return the list of available subcommands,
        positional and optional arguments
        '''
        print "cmdlist: ", cmdlist
        matches = []
        if len(cmdlist) == 1:
            result = self.os_commandhandler.get_command_options("")
            if result != 0:
                return []
            matches = self.os_commandhandler.commands

        return matches

    def get_completions(self, document, complete_event):
        '''
        We override this function from the parent class. It returns
        an iterator.
        '''
        cmdlist = self.parse_document(document)
        completion_options = self.get_current_command_options(cmdlist)

        for option in completion_options:
            yield Completion(option, start_position=0)


