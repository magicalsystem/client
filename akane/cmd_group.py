import click
import client

from libs import api
from libs import ansibleapi


@client.cli.group()
@click.pass_context
def group(ctx):
    pass


@group.command()
@click.pass_context
@click.argument('name')
def add(ctx, name):
    result = ctx.obj['api'].groups_add(name)
    if result:
        click.echo('Group added')
    else:
        click.echo('Something went wrong, please try again')


@group.command()
@click.pass_context
@click.argument('name')
def show(ctx, name):
    status, result = ctx.obj['api'].groups_get(name)
    if status:
        click.echo(result)
    else:
        click.echo("Something went wrong, please try again")


@group.command("del")
@click.pass_context
@click.argument('name')
def delete(ctx, name):
    result = ctx.obj['api'].groups_del(name)

    if result:
        pass #super dziala


@group.command()
@click.pass_context
@click.argument('criteria', nargs=-1)
def list(ctx, criteria):
    criteria = ansibleapi._criteria2dict(criteria)
    click.echo(ctx.obj['api'].groups_get(criteria))