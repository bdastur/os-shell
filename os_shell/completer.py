#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
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
        matches = []

        result = self.os_commandhandler.get_command_options("")
        cmdobj = self.os_commandhandler.commands

        command = []
        for loc in cmdlist:

            if loc.startswith("-") or loc.startswith("--"):
                continue

            command.append(loc)
            if loc in cmdobj:
                result = self.os_commandhandler.get_command_options(command)
                if result != 0:
                    break
                cmdobj = self.os_commandhandler.commands
            else:
                matchstr = r"%s.*" % loc
                for option in cmdobj:
                    if re.match(matchstr, option):
                        matches.append(option)
                return matches

        matches = cmdobj
        optional_args = set()
        for option in self.os_commandhandler.optional_arguments:
            optional_args.add(option[0])

        positional_args = set()
        for option in self.os_commandhandler.positional_arguments:
            positional_args.add(option[0])

        matches.extend(list(positional_args))
        matches.extend(list(optional_args))

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


