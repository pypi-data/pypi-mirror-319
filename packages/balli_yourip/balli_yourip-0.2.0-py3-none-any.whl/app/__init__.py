import click
import requests


@click.command()
@click.option("--name", default="World", help="Name to greet.")
def main(name):
    """A simple CLI tool."""
    response = requests.get("https://httpbin.org/ip")
    ip = response.json()["origin"]
    click.echo(f"Hello, {name}! Your IP is {ip}.")


if __name__ == "__main__":
    main()
