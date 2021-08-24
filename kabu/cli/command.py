import click

from kabu.cli.financial import financial
from kabu.cli.report import report
from kabu.cli.seekinga import seekinga
#from kabu.cli.consensus import Consensus
#from kabu.cli.browser import Browser

@click.group()
def cmd():
    pass

cmd.add_command(financial)
cmd.add_command(seekinga)
cmd.add_command(report)
#cmd.add_command(Browser)
