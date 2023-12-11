#!/usr/bin/env python
"""
This file contains Python functions for custom filters in Ansible.
"""

import re

class FilterModule(object):
    """ Default class to use custom filters in Ansible.
    """

    def filters(self):
        """ Default function for custom filter implementation."""
        return { "ios_vrf_rt": ios_vrf_rt }



def ios_vrf_rt(text_config):
    """ This function receives text string with 'show run' configuration.
    And returns a dictionary with RT imports/export for all VRFs.
    Keys of the dictionary are VRF names.
    """
    pattern_vrf = r"vrf\s+definition\s+(?P<vrf>\S+)"
    regex_vrf = re.compile(pattern_vrf)
    pattern_rt_import = r"route-target\s+import\s+(?P<rt_import>\S+)"
    regex_rt_import = re.compile(pattern_rt_import)
    pattern_rt_export = r"route-target\s+export\s+(?P<rt_export>\S+)"
    regex_rt_export = re.compile(pattern_rt_export)

    text_lines = text_config.split("\n")
    vrfs = {} # Dictionary for results.
    # Keys - VRF names, values: dictionaries with keys "route_import" and "route_export"
    # and values - RT communities

    for line in text_lines:
        match_vrf = regex_vrf.search(line)
        if match_vrf:
            vrf_name = match_vrf.group("vrf")
            vrfs[vrf_name] = {"route_import": [], "route_export": [] }

        match_rt_import = regex_rt_import.search(line)
        if match_rt_import:
            vrfs[vrf_name]["route_import"].append(match_rt_import.group("rt_import"))

        match_rt_export = regex_rt_export.search(line)
        if match_rt_export:
            vrfs[vrf_name]["route_export"].append(match_rt_export.group("rt_export"))

    return vrfs
