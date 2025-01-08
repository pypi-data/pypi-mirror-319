"""CLI Implementation.

Usage:

portia-cli run "add 4 + 8" - run a query
portia-cli plan "add 4 + 8" - plan a query
"""

import click

from portia.config import LogLevel, default_config
from portia.example_tools import example_tool_registry
from portia.runner import Runner
from portia.tool_registry import PortiaToolRegistry


@click.group()
def cli() -> None:
    """Portia CLI."""


@click.command()
@click.argument("query")
def run(query: str) -> None:
    """Run a query."""
    config = default_config()
    config.default_log_level = LogLevel.ERROR
    registry = example_tool_registry
    if config.has_api_key("portia_api_key"):
        registry += PortiaToolRegistry(config)
    runner = Runner(config=config, tool_registry=registry)
    output = runner.run_query(query)
    click.echo(output.model_dump_json(indent=4))


@click.command()
@click.argument("query")
def plan(query: str) -> None:
    """Plan a query."""
    config = default_config()
    config.default_log_level = LogLevel.ERROR
    registry = example_tool_registry
    if config.has_api_key("portia_api_key"):
        registry += PortiaToolRegistry(config)
    runner = Runner(config=config, tool_registry=registry)

    output = runner.plan_query(query)
    click.echo(output.model_dump_json(indent=4))


cli.add_command(run)
cli.add_command(plan)

if __name__ == "__main__":
    cli()
