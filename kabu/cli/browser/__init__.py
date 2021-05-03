import click

from kabu.cli.browser.scrape import scrape

Browser = click.Group('browser', help='selenium rpc')
Browser.add_command(scrape)
