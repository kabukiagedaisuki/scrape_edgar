import click

from kabu.cli.edgar import Edgar
from kabu.cli.consensus import Consensus
from kabu.cli.browser import Browser

@click.group()
def cmd():
    pass

cmd.add_command(Edgar)
cmd.add_command(Consensus)
cmd.add_command(Browser)
