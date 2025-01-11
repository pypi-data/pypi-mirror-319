import click

def print_error(message: str) -> None:
    click.echo(click.style(message, fg='red', bold=True))

def print_success(message: str) -> None:
    click.echo(click.style(message, fg='green', bold=True))

def print_warning(message: str) -> None:
    click.echo(click.style(message, fg='yellow', bold=True))

def print_info(message: str) -> None:
    click.echo(click.style(message, fg='blue', bold=True))

def print_default(message: str) -> None:
    click.echo(click.style(message, fg='white', bold=True))
