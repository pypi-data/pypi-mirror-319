import rich
import rich_click as click

from codegen.cli.analytics.decorators import track_command
from codegen.cli.auth.token_manager import TokenManager


@click.command(name="logout")
@track_command()
def logout_command():
    """Clear stored authentication token."""
    token_manager = TokenManager()
    token_manager.clear_token()
    rich.print("Successfully logged out")
