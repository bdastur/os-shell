#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from os_shell.os_commandhelper import OSCommandHelper


class Resource(object):
    def __init__(self):
        self.command_helper = OSCommandHelper(skip_cache=True)
        self.resource_outputfile = "/tmp/osresource.txt"
        self.images = None
        self.flavors = None

        self.populate_images()
        self.populate_flavors()

    def populate_images(self):
        cmd = "image list --format json".split()
        print "Cache images.."
        self.command_helper.trigger_openstack_cli(
            cmd,
            output_file=self.resource_outputfile)

        with open(self.resource_outputfile, "r") as resource_file:
            try:
                self.images = json.loads(resource_file.read())
            except ValueError:
                self.images = None

    def populate_flavors(self):
        cmd = "flavor list --format json".split()
        print "Cache flavors.."
        self.command_helper.trigger_openstack_cli(
            cmd,
            output_file=self.resource_outputfile)
        with open(self.resource_outputfile, "r") as resource_file:
            try:
                self.flavors = json.loads(resource_file.read())
            except ValueError:
                self.flavors = None

    def get_image_list(self):
        '''
        Return the list of image names.
        '''
        image_names = []

        if self.images is None:
            return (1, None)

        for obj in self.images:
            image_names.append(obj['Name'])

        return (0, image_names)

    def get_flavor_list(self):
        '''
        Return list of flavors.
        '''
        flavor_names = []

        if self.flavors is None:
            return (1, None)

        for obj in self.flavors:
            flavor_names.append(obj['Name'])

        return (0, flavor_names)





