import click
import client

@client.cli.group()
@click.pass_context
def user(ctx):
    pass

@user.command()
@click.pass_context
@click.argument("name")
def add(ctx, name):
    status = ctx.obj['api'].users_update(name)
    click.echo('User added') if status else click.echo('Something went wrong, please try again')

@user.command("del")
@click.pass_context
@click.argument("name")
def delete(ctx, name):
    status, users = ctx.obj['api'].users_get({"name": name})
    click.echo("User deleted") if status else click.echo('Something went wrong, please try again')

@user.command()
@click.pass_context
def list(ctx):
    status, users = ctx.obj['api'].users_get()
    click.echo(users) if status else click.echo('Something went wrong, please try again')

@user.command()
@click.pass_context
@click.argument("name")
def show(ctx, name):
    status, users = ctx.obj['api'].users_get({"name": name})
    click.echo(users) if status else click.echo('Something went wrong, please try again')
