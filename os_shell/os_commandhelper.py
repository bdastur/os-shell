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
    def __init__(self):
        self.help_cmdfile = "/tmp/oshelpoutput.txt"

    def get_openstack_help_options(self, command):
        '''
        Execute the help command. This function  will be
        invoked in a seperate process as we will redirect stdout
        to a file which we will read later.
        '''
        os_command = ["help"]
        if command:
            os_command.extend(command)

        sys.stdout = open(self.help_cmdfile, "w")
        OpenStackShell().run(os_command)


    def parse_cmdoutput_file(self):
        '''
        Parse the help_cmdfile output.
        '''
        try:
            fp = open(self.help_cmdfile, "r")
        except IOError:
            print "Failed to open %s " % self.help_cmdfile
            return (1, None, None)

        optional_arguments = []
        commands = set()

        data = fp.readlines()
        parse_stage = None
        for line in data:
            line = line.strip()
            if re.match("optional arguments:", line):
                # We can start parsing optional arguments.
                parse_stage = 1
            elif re.match("Commands:", line):
                # We can start parsing commands
                parse_stage = 2
            elif parse_stage == 1:
                if re.match(r"--(\w+)", line) or \
                      re.match(r"-(\w+)", line):
                    temp = line.split()
                    option = temp[0]
                    helpstr = " ".join(temp[1:])
                    optional_arguments.append((option, helpstr))
            elif parse_stage == 2:
                temp = line.split()
                command = temp[0]
                commands.add(command)

        cmdlist = list(commands)
        return (0, sorted(optional_arguments, key=lambda k: k[0]),
                sorted(cmdlist))

    def get_command_options(self, cmdlist):
        '''
        Given a prompt it will return the available options
        eg: if cmd is empty it will list all the avilable comamnds at
            the top level.
            If cmd is "server", it will list all the commands within server.
        '''
        helper_process = Process(target=self.get_openstack_help_options,
                                 args=(cmdlist,))
        helper_process.start()
        helper_process.join()
        (result, optional_args, commands) = self.parse_cmdoutput_file()
        if result != 0:
            print "Failed to parse"
            return (1, None, None)

        return (0, optional_args, commands)







