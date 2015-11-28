import click
import cmd_user

@cmd_user.user.group()
def key():
    pass

@key.command()
@click.argument("username")
@click.argument("pubkey", type=click.File('rb'))
def add(username, pubkey):
    pk = pubkey.read()  # read public key from file or stdin
    # do sth with pk
    click.secho("Added key to %s" % username, fg='green')