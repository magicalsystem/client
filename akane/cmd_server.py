import click
import client

from libs import api
from libs import ansibleapi


@client.cli.group()
@click.pass_context
def server(ctx):
    pass


@server.command()
@click.pass_context
@click.argument('name')
def add(ctx, name):
    ctx.obj['api'].servers_update([{'name': name}])

@server.command('del')
@click.pass_context
@click.argument('name')
def delete(ctx, name):
    ctx.obj['api'].servers_del(name)

@server.command()
@click.pass_context
@click.argument('criteria', nargs=-1)
def list(ctx, criteria):
    criteria = ansibleapi._criteria2dict(criteria)
    click.echo(ctx.obj['api'].servers_get(criteria))

@server.command()
@click.pass_context
@click.argument('name')
def show(ctx, name):
    click.echo(ctx.obj['api'].servers_get({'_id': [name]}))