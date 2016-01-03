import tempfile
import json

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

@ansible.command()
@click.pass_context
@click.option('--list', 'list_flag', is_flag=True)
@click.option('--host')
def di(ctx, list_flag, host):
    if list_flag and not host:
        _, groups = ctx.obj['api'].groups_get()
        _, hosts = ctx.obj['api'].servers_get()

        click.echo(json.dumps(libs.ansibleapi.dynamic_inventory(groups, hosts)))
    else:
        click.secho("Wrong dynamic inventory arguments", fg='red')
        ctx.exit(1)

@ansible.command('temp-di')
@click.pass_context
@click.argument('filter', 'fltr')
def temp_di(ctx, crit):
   inv = tempfile.NamedTemporaryFile('wrb')
   _, groups = ctx.obj['api'].groups_get()
   pass


@ansible.command()
@click.pass_context
def discover(ctx):
    libs.ansibleapi.discover()

