import json
import os
import pathlib
import sys
from typing import Dict, List, Optional

import click
import requests
import yaml
from rich.console import Console
from rich.markup import escape

from lila.config import Config
from lila.runner import TestRunner, collect_test_cases
from lila.utils import parse_tags
from lila.version import get_version


def validate_content(content: str, server_url: str) -> None:
    try:
        yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise ValueError(f"Provided content is not a valid YAML: {e}")

    ret = requests.post(
        f"{server_url}/api/v1/testcase-validations",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {os.environ['LILA_API_KEY']}",
        },
        json={"content": content},
    )
    raise_for_status(ret)
    if ret.status_code == 200:
        data = ret.json()
        if data["valid"]:
            return

        raise ValueError(
            f"Provided content is not a valid Lila test case: {data['message']}"
        )


def find_parsing_errors(test_paths: List[str], server_url: str) -> Dict[str, str]:
    invalid_tests = {}
    for path in test_paths:
        with open(path, "r") as f:
            content = f.read()
            try:
                validate_content(content, server_url)
            except ValueError as e:
                invalid_tests[path] = str(e)

    return invalid_tests


def raise_for_status(response: requests.Response):
    try:
        response.raise_for_status()
    except requests.RequestException as e:
        try:
            data = response.json()
            raise RuntimeError(f"Error: {data}") from e
        except json.JSONDecodeError:
            raise RuntimeError(f"Error: {response.text}") from e


@click.group()
def cli():
    """Lila CLI tool."""
    console = Console()
    console.print("Lila CLI ", style="bold violet", end="")
    console.print(f"[not bold violet]{get_version()}[/]", end="\n\n")


def collect(path) -> List[str]:
    """
    Find all YAML files in a given path. If path is a file, return it if it's a YAML file.
    If path is a directory, recursively search for all YAML files within it.

    Args:
        path (str): Path to file or directory

    Returns:
        list: List of paths to YAML files found
    """
    yaml_extensions = (".yaml", ".yml")
    result = []

    # Convert path to Path object for easier handling
    path_obj = pathlib.Path(path)

    # If path is a file, check if it's a YAML file
    if path_obj.is_file():
        if path_obj.suffix.lower() in yaml_extensions:
            return [str(path_obj)]
        return []

    # If path is a directory, walk through it recursively
    if path_obj.is_dir():
        for root, _, files in os.walk(path):
            for file in files:
                file_path = pathlib.Path(root) / file
                if file_path.suffix.lower() in yaml_extensions:
                    result.append(str(file_path))

    return sorted(result)  # Sort for consistent output


def _get_config(config_file: Optional[str]) -> Config:
    if not config_file:
        if os.path.exists("lila.toml"):
            config_file = "lila.toml"
        else:
            return Config.default()
    elif not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")

    return Config.from_toml_file(config_file)


@cli.command()
@click.argument("path", type=str, required=True)
@click.option(
    "--tags",
    type=str,
    help="Comma-separated list of tags",
    required=False,
)
@click.option("--exclude-tags", type=str, help="Exclude tests by tags")
@click.option("--config", type=str, help="Path to the Lila config file", required=False)
@click.option(
    "--browser-state", type=str, help="Path to the browser state file", required=False
)
def run(
    path: str,
    tags: str,
    exclude_tags: str,
    config: Optional[str],
    browser_state: Optional[str],
):
    """Run a Lila test suite."""
    console = Console()
    try:
        config_obj = _get_config(config)
    except FileNotFoundError as e:
        console.print(str(e), style="bold red")

    tag_list = []
    if tags:
        try:
            tag_list = parse_tags(tags)
        except ValueError as e:
            console.print(str(e), style="bold red")
            return

    exclude_tag_list = []
    if exclude_tags:
        try:
            exclude_tag_list = parse_tags(exclude_tags)
        except ValueError as e:
            console.print(str(e), style="bold red")
            return

    # If intersection of tags and exclude_tags is not empty, raise an error
    if set(tag_list) & set(exclude_tag_list):
        console.print(
            escape(
                f"Tags and exclude-tags cannot have common elements: {tag_list} and {exclude_tag_list}"
            ),
            style="bold red",
        )
        return

    if browser_state and not os.path.exists(browser_state):
        console.print(
            f"Browser state file not found: {browser_state}", style="bold red"
        )
        return

    test_files = collect(path)
    if not test_files:
        console.print(
            f"No YAML files found in the provided path: {path}", style="bold red"
        )
        return

    invalid_files = find_parsing_errors(test_files, config_obj.runtime.server_url)
    if invalid_files:
        console.print("=== Parsing Errors ===", style="bold")
        for path, error in invalid_files.items():
            console.print(f"File: [bold]{path}[/]", style="bold red")
            console.print(f"Error: {error}", style="bold red")
        return

    testcases = collect_test_cases(test_files, tag_list, exclude_tag_list)

    if not testcases:
        console.print(
            "No test cases found with the provided path and the provided params",
            style="bold red",
        )
        return

    runner = TestRunner(testcases)
    success = runner.run_tests(config_obj, browser_state)
    if not success:
        sys.exit(1)


@cli.command()
def init():
    """Initialize a Lila testing template."""
    click.echo("Initializing the application...")
