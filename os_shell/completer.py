#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from prompt_toolkit.completion import Completer, Completion


class OSCompleter(Completer):
    '''
    Our Custom Completer, which is a subclass of the prompt_toolkit
    Completer class.
    '''
    def __init__(self, os_commandhandler, resource):
        self.os_commandhandler = os_commandhandler
        self.os_resource = resource

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

    def get_variable_resource_options(self, cmds):
        matches = []
        if len(cmds) <= 1:
            return (1, matches)

        option = cmds[len(cmds) - 1]
        if option == "--image".strip():
            (ret, matches) = self.os_resource.get_image_list()
            if ret == 0:
                return (0, matches)

        elif option == "--flavor".strip():
            (ret, matches) = self.os_resource.get_flavor_list()
            if ret == 0:
                return (0, matches)

        elif option == "--nic".strip():
            (ret, matches) = self.os_resource.get_network_list()
            if ret == 0:
                return (0, matches)

        return (1, matches)

    def get_current_command_options(self, cmdlist):
        '''
        The function will return the list of available subcommands,
        positional and optional arguments
        '''
        matches = []

        # At anytime we only deal with the most recent command.
        # Since we have already processed the previous commands.
        processed_cmds = cmdlist[:-1]
        (ret, matches) = self.get_variable_resource_options(processed_cmds)
        if ret == 0:
            return matches

        # Get all the available cmd options to begin with.
        if len(cmdlist) <= 1:
            result = self.os_commandhandler.get_command_options("")

        # Get the latest command options.
        cmdobj = self.os_commandhandler.get_current_commands()

        command = []
        for loc in cmdlist:
            command.append(loc)
            if loc in processed_cmds:
                # if we have processed this token, skip it.
                continue

            # If we are parsing optional arguments, we do not need
            # to update the cached options. We will use existing cache.
            # also only return optional argument matches.
            if loc.startswith("-") or loc.startswith("--"):
                matchstr = r"%s.*" % loc
                cmdopts = \
                    self.os_commandhandler.get_current_optional_arguments()
                for option in cmdopts:
                    if re.match(matchstr, option):
                        matches.append(option)
                return matches

            # If the token is actually present in the options, we will
            # retrieve the relevant options for this command.
            if loc in cmdobj:
                result = self.os_commandhandler.get_command_options(command)
                if result != 0:
                    break
                cmdobj = self.os_commandhandler.get_current_commands()
            else:
                # If we could not match the complete token, try a partial
                # match from available options at the moment.
                matchstr = r"%s.*" % loc
                for option in cmdobj:
                    if re.match(matchstr, option):
                        matches.append(option)
                return matches

        matches = cmdobj
        optional_args = self.os_commandhandler.get_current_optional_arguments()

        positional_args = \
            self.os_commandhandler.get_current_positional_arguments()

        matches.extend(positional_args)
        matches.extend(optional_args)

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


