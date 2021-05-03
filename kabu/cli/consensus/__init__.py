import click

from kabu.cli.consensus.estimate import estimate

Consensus = click.Group('consensus', help='analysis consensus estimate')
Consensus.add_command(estimate)
