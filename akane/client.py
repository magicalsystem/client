import sys

import click
from libs.config import read_config
from libs.api import API

# declare main command group
@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj['cfg'] = read_config()
    ctx.obj['api'] = API(ctx.obj['cfg'])

# import commands
import cmd_user
import cmd_group
import cmd_server
# import ansible module
import cmd_ansible



