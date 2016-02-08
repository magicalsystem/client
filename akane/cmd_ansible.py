import tempfile
import json
import os
import stat

import click

import client
import libs.ansibleapi
from libs.config import read_config
from libs.api import API

_ANSIBLE_DI_TPL_ = """#!/usr/bin/env bash

./akanectl ansible di %s $@
"""


def _create_di(criteria):
    inv = tempfile.NamedTemporaryFile('wrb', delete=False)
    inv.write(_ANSIBLE_DI_TPL_ % criteria)
    inv.close()

    mode = os.stat(inv.name).st_mode
    os.chmod(inv.name, mode | stat.S_IEXEC)
    return inv.name

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
@click.argument('criteria', nargs=-1)
@click.option('--list', 'list_flag', is_flag=True)
@click.option('--host')
def di(ctx, criteria, list_flag, host):
    c = libs.ansibleapi._criteria2dict(criteria)

    if list_flag and not host:
        _, di = ctx.obj['api'].ansible_di(c)
        click.echo(json.dumps(di))
    else:
        click.secho("Wrong dynamic inventory arguments", fg='red')
        ctx.exit(1)

@ansible.command('temp-di')
@click.pass_context
@click.argument('criteria', nargs=-1)
def temp_di(ctx, criteria):
    click.echo(_create_di(criteria))


@ansible.command()
@click.pass_context
@click.argument('hostname')
def discover(ctx, hostname):
     r = libs.ansibleapi.discover(_create_di("name=%s" % hostname))
     # todo: populate db with received data
