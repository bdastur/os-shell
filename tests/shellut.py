#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from os_commandhelper import OSCommandHelper


class ShellUt(unittest.TestCase):
    def get_command_options(self, cmdlist):
        cmdhelper = OSCommandHelper()
        self.failUnless(cmdhelper is not None)

        result = cmdhelper.get_command_options(cmdlist)
        self.failUnless(result == 0)

        for option in cmdhelper.optional_arguments:
            print "Option: ", option[0]

        for option in cmdhelper.positional_arguments:
            print "%s: %s" % (option[0], option[1])

        for cmd in cmdhelper.commands:
            print "Command: ", cmd

    def test_get_command_options_toplevel(self):
        print "Test get_command_options - level 1"
        cmdhelper = OSCommandHelper()
        self.failUnless(cmdhelper is not None)

        result = cmdhelper.get_command_options("")
        self.failUnless(result == 0)

        for option in cmdhelper.optional_arguments:
            print "Option: ", option[0]

        for cmd in cmdhelper.commands:
            print "Command: ", cmd

    def test_get_command_options_server(self):
        print "Test get_command_options - level 2"
        cmdhelper = OSCommandHelper()
        self.failUnless(cmdhelper is not None)

        result = cmdhelper.get_command_options(["server"])
        self.failUnless(result == 0)

        for option in cmdhelper.optional_arguments:
            print "Option: ", option[0]

        for cmd in cmdhelper.commands:
            print "Command: ", cmd

    def test_get_command_options_server_create(self):
        print "Test get_command options - level 3"
        self.get_command_options(["server", "create"])


    def test_get_command_options_image(self):
        print "Test get command options - image"
        self.get_command_options(["image"])
