#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
from os_shell.os_commandhelper import OSCommandHelper


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

    def test_get_command_options_cached(self):
        print "Test get command options - cached"
        cmdhelper = OSCommandHelper()
        self.failUnless(cmdhelper is not None)

        result = cmdhelper.get_command_options("")
        self.failUnless(result == 0)
        for cmd in cmdhelper.commands:
            print "Command: ", cmd

        print "Second invocation will get from cache......."
        result = cmdhelper.get_command_options("")
        self.failUnless(result == 0)
        for cmd in cmdhelper.commands:
            print "Command: ", cmd

        result = cmdhelper.get_command_options(["server"])
        self.failUnless(result == 0)
        for cmd in cmdhelper.commands:
            print "Command: ", cmd

    def test_cachekey_from_cmdlist(self):
        print "Test api to get cachekey from cmdlist"
        cmdhelper = OSCommandHelper()
        self.failUnless(cmdhelper is not None)

        cmdlist = ""
        cachekey = cmdhelper.get_cachekey_from_cmdlist(cmdlist)
        print "cachekey:", cachekey, "len: ", len(cachekey)

        cmdlist = ["server", "create"]
        cachekey = cmdhelper.get_cachekey_from_cmdlist(cmdlist)
        print "cachekey:", cachekey, "len: ", len(cachekey)

    def test_trigger_openstack_cli(self):
        print "Test trigger_openstack_cli"
        cmd = "image list --format json".split()
        output_file = "/tmp/osresource.txt"
        cmdhelper = OSCommandHelper()
        self.failUnless(cmdhelper is not None)

        cmdhelper.trigger_openstack_cli(cmd,
                                        output_file=output_file)

        with open(output_file, "r") as resource_file:
            try:
                data = json.loads(resource_file.read())
            except ValueError:
                data = None

        print "Data: ", data

    def test_trigger_openstack_cli_flavor(self):
        print "Test trigger openstack cli - flavor list"
        cmd = "flavor list --format json".split()
        output_file = "/tmp/osresource.txt"
        cmdhelper = OSCommandHelper()
        self.failUnless(cmdhelper is not None)

        cmdhelper.trigger_openstack_cli(cmd,
                                        output_file=output_file)
        with open(output_file, "r") as resource_file:
            try:
                data = json.loads(resource_file.read())
            except ValueError:
                data = None

        print "Data: ", data

