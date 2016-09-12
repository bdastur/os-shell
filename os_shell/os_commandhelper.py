#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
The class works as an interface to the Openstack Client.
It serves two purposes.
1. It will be used by the custome Completer to get the available
   options for a given command.
2. It will be invoked to actually execute the tasks.

In trun it will invoke the OpenstackShell's run method to execute the tasks.
'''

import sys
import re
from openstackclient.shell import OpenStackShell
from multiprocessing import Process


class OSCommandHelper(object):
    '''
    The class to interface with Openstack Client
    '''
    def __init__(self, skip_cache=False):
        self.help_cmdfile = "/tmp/oshelpoutput.txt"

        self.cached_optional_arguments = {}
        self.cached_commands = {}
        self.cached_positional_arguments = {}
        self.cached_output_formatters = {}

        self.optional_arguments = []
        self.positional_arguments = []
        self.commands = []
        self.output_formatters = []

        # Let's initially cache the toplevel commands, to remove initial
        # latency during command input.
        if not skip_cache:
            print "Creating initial cache.."
            ret = self.get_command_options("")
            if ret != 0:
                print "Failed to cache os commands"

    def get_current_optional_arguments(self):
        '''
        Return a list of current optional arguments.
        '''
        optional_args = []
        for option in self.optional_arguments:
            optional_args.append(option[0])

        return optional_args

    def get_current_commands(self):
        '''
        Return the current commands
        '''
        return self.commands

    def get_current_positional_arguments(self):
        '''
        Return positional arguments
        '''
        positional_args = []
        for option in self.positional_arguments:
            positional_args.append(option[0])

        return positional_args

    def get_openstack_help_options(self, command):
        '''
        Execute the help command. This function  will be
        invoked in a seperate process as we will redirect stdout
        to a file which we will read later.
        '''
        os_command = ["help"]
        if command:
            os_command.extend(command)

        #print "OS Command: ", os_command

        sys.stdout = open(self.help_cmdfile, "w")
        OpenStackShell().run(os_command)

    def execute_openstack_cli(self, cmdlist,
                              output_file=None):
        '''
        Execute the Openstack command.
        '''
        if output_file:
            try:
                sys.stdout = open(output_file, "w")
            except IOError:
                print "Failed to open %s " % output_file
                return

        trimmed_cmdlist = []
        for cmd in cmdlist:
            if cmd != "" and cmd != " ":
                trimmed_cmdlist.append(cmd)
        try:
            OpenStackShell().run(trimmed_cmdlist)
        except Exception as osexception:
            print "Failed operation [%s], [%s]" % \
                (trimmed_cmdlist, osexception)

    def trigger_openstack_cli(self,
                              cmdlist,
                              output_file=None):
        '''
        Trigger openstack cli in a new process.
        '''
        helper_process = Process(target=self.execute_openstack_cli,
                                 args=(cmdlist, output_file,))
        helper_process.start()
        helper_process.join()

    def get_cachekey_from_cmdlist(self, cmdlist):
        '''
        Return a string that can be used as a key to index
        the cached commands and arguments.
        '''
        cachekey = "help"
        for command in cmdlist:
            cachekey += "_" + command

        return cachekey

    def update_current_options_from_cache(self, cachekey):
        '''
        If we have cached options then we use them.
        '''

        if self.cached_commands.get(cachekey, None) is not None:
            self.commands = self.cached_commands[cachekey]
            self.optional_arguments = self.cached_optional_arguments[cachekey]
            self.positional_arguments = \
                self.cached_positional_arguments[cachekey]
            return 0

        self.cached_commands[cachekey] = []
        self.cached_optional_arguments[cachekey] = []
        self.cached_positional_arguments[cachekey] = []
        return 1

    def parse_cmdoutput_file(self, cachekey):
        '''
        Parse the help_cmdfile output.
        '''
        try:
            filehandle = open(self.help_cmdfile, "r")
        except IOError:
            print "Failed to open %s " % self.help_cmdfile
            return 1

        commands = set()

        data = filehandle.readlines()
        filehandle.close()
        parse_stage = None
        for line in data:
            line = line.strip()

            if not line:
                continue

            if re.match("optional arguments:", line):
                # We can start parsing optional arguments.
                #print "Matched optional, set stage to 1"
                parse_stage = 1
            elif re.match("Commands:", line):
                # We can start parsing commands
                #print "Matched, set stage 2"
                parse_stage = 2
            elif re.match(r"Command .* matches:", line):
                parse_stage = 3
            elif re.match(r"positional arguments:", line):
                #print "Match positional args section, stage set to 4"
                parse_stage = 4
            elif re.match(r"output formatters:", line):
                parse_stage = 5
            elif parse_stage == 1:
                if re.match(r"--(\w+)", line) or \
                      re.match(r"-(\w+)", line):
                    temp = line.split()
                    option = temp[0]
                    helpstr = " ".join(temp[1:])
                    self.cached_optional_arguments[cachekey].append(
                        (option, helpstr))
            elif parse_stage == 2:
                temp = line.split()
                command = temp[0]
                commands.add(command)
            elif parse_stage == 3:
                temp = line.split()
                command = temp[1]
                commands.add(command)
            elif parse_stage == 4:
                temp = line.split()
                option = temp[0]
                helpstr = " ".join(temp[1:])
                self.cached_positional_arguments[cachekey].append(
                    (option, helpstr))

        self.cached_commands[cachekey] = sorted(list(commands))

        ret = self.update_current_options_from_cache(cachekey)
        if ret != 0:
            return 1

        return 0

    def get_command_options(self, cmdlist):
        '''
        Given a prompt it will return the available options
        eg: if cmd is empty it will list all the avilable comamnds at
            the top level.
            If cmd is "server", it will list all the commands within server.
        '''
        cachekey = self.get_cachekey_from_cmdlist(cmdlist)
        ret = self.update_current_options_from_cache(cachekey)
        if ret == 0:
            return 0

        helper_process = Process(target=self.get_openstack_help_options,
                                 args=(cmdlist,))
        helper_process.start()
        helper_process.join()

        result = self.parse_cmdoutput_file(cachekey)

        if result != 0:
            print "Failed to parse"
            return 1

        return 0
