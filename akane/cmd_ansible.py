import tempfile

import click

import client
import libs.ansibleapi
from libs.config import read_config
from libs.api import API


@client.cli.group()
@click.pass_context
def ansible(ctx):
    pass


@ansible.command('import')
@click.pass_context
@click.argument("inventory", type=click.File('rb'))
def import_inventory(ctx, inventory):
    if inventory.name == '<stdin>':
        click.echo("Reading inventory file from stdin")
        _inv = inventory.read()
        inventory = tempfile.NamedTemporaryFile('wrb')
        inventory.write(_inv)
        inventory.seek(0)
    else:
        click.echo("Reading inventory file from %s" % inventory.name)
    
    hosts, groups = libs.ansibleapi.parse_inventory(inventory.name)
    
    if ctx.obj['api'].groups_update(groups):
        click.secho("Groups updated!", fg='green')
    else:
        click.secho("Error during group_update procedure", fg='red')
        ctx.exit(1)

    if ctx.obj['api'].servers_update(hosts):
        click.secho("Hosts updated!", fg='green')
    else:
        click.secho("Error during hosts_update procedure", fg='red')
        ctx.exit(1)


