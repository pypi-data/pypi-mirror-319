import click
import asyncio
from rich.console import Console
from rich.table import Table
from rich.spinner import Spinner
from rich.live import Live
import time
from foocheck.utils import check_username
from foocheck.sites import SITES

console = Console()

async def check_sites(username, category):
    """Check username availability across a list of networks in parallel.

    Args:
        username (str): The username to check.
        category (list): A category of sites to check.

    Returns:
        list: A list of tuples containing the network name and status.
    """
    if category == "all":
        category_sites = SITES
    else:
        category_sites = [site for site in SITES if site["category"]==category]
    tasks = [check_username(username, site) for site in category_sites]

    # Display a spinner while waiting for results
    with Live(Spinner("dots", text="Checking websites..."), console=console, transient=True):
        results = await asyncio.gather(*tasks)

    return [(category_sites[i], results[i]) for i in range(len(category_sites))]

def display_single_result(site, username, status):
    """Display the result for a single network.

    Args:
        site (dict): The website info.
        status (str): The status of the username ("Taken", "Available", "Unknown", or "Error").
    """
    if status == "Available":
        console.print(f"[green][✓] {site["name"]}[/green]:  {site["url"].format(username)}")
    elif status == "Taken":
        console.print(f"[red][✗] {site["name"]}[/red]:  {site["url"].format(username)}")
    else:
        console.print(f"[yellow][?] {site["name"]}[/yellow]:  {site["url"].format(username)}")

def display_results(username, results):
    """Display the summary of username availability checks.

    Args:
        username (str): The username to check.
        results (list): A list of tuples containing the website info and status.
    """
    sorted_results = sorted(results, key=lambda x: x[0]["name"])
    for site, status in sorted_results:
        time.sleep(0.5)
        display_single_result(site, username, status)

@click.command()
@click.argument("username")
@click.option(
    "--category",
    type=click.Choice(["social",
                       "dev",
                       "streaming",
                       "gaming",
                       "forum",
                       "other",
                       "blog",
                       "job",
                       "all"], case_sensitive=False),
    default="all",
    help="Category of platforms to check (default: all).",
)
def main(username, category):
    """Check if a username is taken on various social networks and platforms.

    Args:
        username (str): The username to check.
        category (str): The category of platforms to check.
    """
    # console.print(f"[bold]Foocheck - Checking username: {username}[/bold]\n")
    results = asyncio.run(check_sites(username, category))
    display_results(username, results)

if __name__ == "__main__":
    main()
