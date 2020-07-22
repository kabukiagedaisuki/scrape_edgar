import click
from .ticker2cik.command import cmd as t2c_cmd
from .finance.command import cmd as finance_cmd

@click.group()
def cmd():
    pass

cmd.add_command(t2c_cmd)
cmd.add_command(finance_cmd)
