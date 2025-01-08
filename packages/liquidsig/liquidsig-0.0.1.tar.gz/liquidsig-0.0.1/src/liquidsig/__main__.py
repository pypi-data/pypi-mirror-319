"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """Liquidsig."""


if __name__ == "__main__":
    main(prog_name="liquidsig")  # pragma: no cover
