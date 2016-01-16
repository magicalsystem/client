import os
import json

import ansible.inventory
import ansible.runner


def parse_inventory(inv_path):
    inv = ansible.inventory.Inventory(inv_path)
 
    hosts = list()
    for h in inv.get_hosts():
        hosts.append({
                'name': h.name,
                'vars': h.vars,
                'groups': [g.name for g in h.groups]
                })

    groups = list()
    for g in inv.get_groups():
        if g.name in ['all', 'ungrouped']:
            continue
        groups.append({
                'name': g.name,
                'vars': g.vars,
                'ancestors': [a.name \
                        for a in g.get_ancestors() \
                        if a.name != 'all']
                })

    return hosts, groups


def discover(invfile):
    inv = ansible.inventory.Inventory(invfile)
    resp = ansible.runner.Runner(**{
        'pattern': '*',
        'module_name': 'setup',
        'inventory': inv,
        'remote_user': os.getenv('USER'),
        'private_key_file': '~/.ssh/id_rsa'
        }).run()
    
    return resp
