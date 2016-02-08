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
        click.echo('Ale sie super dodalo')
    else:
        pass
    #scierwiasto sie dodalo


@group.command()
@click.pass_context
@click.argument('name')
def show(ctx, name):
    result = ctx.obj['api'].groups_get(name)

    if result:
        pass #tutaj wyswietl result


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