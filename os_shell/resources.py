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
        self.networks = None

        self.populate_images()
        self.populate_flavors()
        self.populate_networks()

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

    def populate_networks(self):
        cmd = "network list --format json".split()
        print "Cache Networks.."
        self.command_helper.trigger_openstack_cli(
            cmd,
            output_file=self.resource_outputfile)
        with open(self.resource_outputfile, "r") as resource_file:
            try:
                self.networks = json.loads(resource_file.read())
            except ValueError:
                self.networks = None

    def get_image_list(self):
        '''
        Return the list of image names.
        '''
        image_names = []

        if self.images is None:
            return (1, image_names)

        for obj in self.images:
            image_names.append(obj['Name'])

        return (0, image_names)

    def get_flavor_list(self):
        '''
        Return list of flavors.
        '''
        flavor_names = []

        if self.flavors is None:
            return (1, flavor_names)

        for obj in self.flavors:
            flavor_names.append(obj['Name'])

        return (0, flavor_names)

    def get_network_list(self):
        network_ids = []

        if self.networks is None:
            return (1, network_ids)

        for obj in self.networks:
            netid_str = "net-id=%s" % obj['ID']
            network_ids.append(netid_str)

        return (0, network_ids)



