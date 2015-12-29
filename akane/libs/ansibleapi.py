import ansible.inventory

def parse_inventory(inv_path):
    inv = ansible.inventory.Inventory(inv_path)
 
    hosts = dict()
    for h in inv.get_hosts():
        hosts[h.name] = {
                'vars': h.vars,
                'groups': [g.name for g in h.groups]
                }

    groups = dict()
    for g in inv.get_groups():
        if g.name in ['all', 'ungrouped']:
            continue
        groups[g.name] = {
                'vars': g.vars,
                'ancestors': [a.name \
                        for a in g.get_ancestors() \
                        if a.name != 'all']
                }

    return hosts, groups
