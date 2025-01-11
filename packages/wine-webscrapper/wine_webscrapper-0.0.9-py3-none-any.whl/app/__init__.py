import click
from sqlalchemy import create_engine
from app.utils import print_success
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///database.sqlite", echo=True)
Session = sessionmaker(engine)


@click.group()
def cli() -> None:
    """The helper CLI for scrapper."""


@cli.command()
def run() -> None:
    """Run scrapping process."""

    from app.db import Base
    Base.metadata.create_all(engine)    
    print_success("Initialized the database.")
