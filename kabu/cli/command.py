import click

from kabu.cli.edgar import Edgar
#from kabu.cli.consensus import Consensus

@click.group()
def cmd():
    pass

cmd.add_command(Edgar)
#cmd.add_command(Consensus)
