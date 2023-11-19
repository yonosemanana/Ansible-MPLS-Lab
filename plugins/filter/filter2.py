#!/usr/bin/env python

import re

class FilterModule(object):

    def filters(self):
        return { "rt_diff": rt_diff }


def rt_diff(int_vrf_list, run_vrf_dict):
    """ Compare list of VRFs which should be configured based on YAML config file
    with dictionary of VRF existing on the router"""

    config_updates = [] # list of dictionaries with RT "import" and "export" communities to add and delete
    
    # Looping through intended VRF list from the lists defined in host_vars/<host>.yaml files
    for int_vrf in int_vrf_list: 
        vrf_name = int_vrf['name']
        vrf_rd = int_vrf['rd']
        vrf_descr = int_vrf['description']

        vrf_update = {'name': vrf_name,
                      'description': vrf_descr,
                      'rd': vrf_rd }

        # Getting data about the VRF from running config. If VRF doesn't exist, dictionary with empty RT lists is returned
        run_vrf = run_vrf_dict.get(vrf_name, {'route_export': [], 'route_import': [] } )

        int_vrf_rti = set(int_vrf['route_import']) # Convert list of RT import of intended VRF to set
        run_vrf_rti = set(run_vrf['route_import']) # Convert list of RT import of running VRF to set

        int_vrf_rte = set(int_vrf['route_export']) # Convert list of RT export of intended VRF to set
        run_vrf_rte = set(run_vrf['route_export']) # Convert list of RT export of running VRF to set

        config_update = {'add_rti': sorted(list(int_vrf_rti - run_vrf_rti)),
                         'del_rti': sorted(list(run_vrf_rti - int_vrf_rti)),
                         'add_rte': sorted(list(int_vrf_rte - run_vrf_rte)),
                         'del_rte': sorted(list(run_vrf_rte - int_vrf_rte)) }

        vrf_update.update(config_update)

        config_updates.append(vrf_update)

    return config_updates



