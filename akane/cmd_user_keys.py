import click
import cmd_user
import libs.auth

@cmd_user.user.group()
def key():
    pass

@key.command()
@click.pass_context
@click.argument("username")
@click.argument("pubkey", type=click.File('rb'))
def add(ctx, username, pubkey):
    pk = pubkey.read()  # read public key from file or stdin
    ctx.obj['api'].key_add(username, pk)
    click.secho("Added key to %s" % username, fg='green')

@key.command("del")
@click.argument("username")
@click.argument("number", type=int)
def delete(username, number):
    click.secho("Deleted key from {username}".format(username=username),
                fg='green')

@key.command()
@click.argument("username")
def list(username):
    pass

@key.command()
@click.argument("username")
@click.argument("number", type=int)
def show(username, number):
    pass

@key.command()
@click.pass_context
def verify(ctx):
    if ctx.obj['api'].verify():
        click.secho("Access verified successfully", fg="green")
    else:
        click.secho("Access denied", fg="red")
        ctx.exit(1)
