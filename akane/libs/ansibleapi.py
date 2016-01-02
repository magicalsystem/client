import ansible.inventory

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


def dynamic_inventory(groups, hosts):
    inv = dict()
    ancestors = dict()

    for g in groups:
        inv[g['name']] = {
                'hosts': list(),
                'vars': g['vars'],
                }
        ancestors[g['name']] = g['ancestors']

    inv['_meta'] = {'hostvars': dict()}
    
    for h in hosts:
        inv['_meta']['hostvars'][h['name']] = h['vars']
        
        for g in h['groups']:
            inv[g]['hosts'].append(h['name'])

            #  append to ancestor group
            for a in ancestors[g]:
                if h['name'] not in inv[a]['hosts']:
                    inv[a]['hosts'].append(h['name'])
    return inv
