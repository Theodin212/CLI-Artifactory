import click
import requests
from API import ArtifactoryClient

@click.group()
@click.option('--base-url', prompt=True, help="This is the URL of the Artifactory instance.")
@click.pass_context
def cli(ctx, base_url):
    """Command Line Interface to manage Artifactory SaaS instance."""
    # Prompt the user for their token
    token = ArtifactoryClient.prompt_for_token()
    ctx.obj = ArtifactoryClient(base_url, token)

def authenticate(base_url, username, password):
    """
    Authenticate with Artifactory using username and password to get a token.

    Args:
        base_url (str): The Artifactory base URL.
        username (str): Username for login.
        password (str): Password for login.

    Returns:
        str: Authentication token.
    """
    url = f"{base_url}/api/security/token"
    data = {
        "username": username,
        "password": password,
        "scope": "member-of-groups:*",
        "expires_in": 1800
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()["access_token"]

@cli.command()
@click.pass_context
def ping(ctx):
    """Check system connectivity."""
    result = ctx.obj.ping()
    click.echo(result)

@cli.command()
@click.pass_context
def version(ctx):
    """Gets the system version."""
    result = ctx.obj.get_version()
    click.echo(result)

@cli.command()
@click.option('--username', prompt=True, help="Username for the new user.")
@click.option('--email', prompt=True, help="Email for the new user.")
@click.pass_context
def create_user(ctx, username, email):
    """Create a new user."""
    result = ctx.obj.create_user(username, email)
    click.echo(result)

@cli.command()
@click.option('--username', prompt=True, help="Name of the user to delete.")
@click.pass_context
def delete_user(ctx, username):
    """Delete an existing user."""
    result = ctx.obj.delete_user(username)
    click.echo(result)

@cli.command()
@click.pass_context
def list_repos(ctx):
    """List all repositories."""
    result = ctx.obj.list_repositories()
    click.echo(result)

if _name_ == '_main_':
    cli()