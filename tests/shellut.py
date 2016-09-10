#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from os_commandhelper import OSCommandHelper


class ShellUt(unittest.TestCase):
    def test_get_command_options(self):
        print "Test get_command_options"
        cmdhelper = OSCommandHelper()
        self.failUnless(cmdhelper is not None)

        (result, options, commands) = \
            cmdhelper.get_command_options("")
        for option in options:
            print "Option: ", option[0]

        for cmd in commands:
            print "Command: ", cmd

