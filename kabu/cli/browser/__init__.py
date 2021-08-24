import click

from kabu.cli.browser.scrape import scrape
from kabu.cli.browser.allticker import allticker

Browser = click.Group('browser', help='selenium rpc')
Browser.add_command(scrape)
Browser.add_command(allticker)
