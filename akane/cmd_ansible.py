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
def import_inventory(ctx, inv):
    hosts, groups = libs.ansibleapi.parse_inventory(inv.name)

