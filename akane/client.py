import click

# declare main command group
@click.group()
def cli():
    pass

# import commands
import cmd_user

@cli.group()
def server():
    pass

@cli.group()
def role():
    pass


