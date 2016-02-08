import click
import client

@client.cli.group()
@click.pass_context
def user(ctx):
    pass

@user.command()
@click.pass_context
def add(ctx):
    click.echo("Added user")

@user.command("del")
def delete():
    click.echo("Deleted user")

@user.command()
@click.pass_context
def list(ctx):
    users = ctx.obj['api'].users_get()

    click.echo(users)

@user.command()
def show():
    click.echo("Information about user")

import cmd_user_keys
