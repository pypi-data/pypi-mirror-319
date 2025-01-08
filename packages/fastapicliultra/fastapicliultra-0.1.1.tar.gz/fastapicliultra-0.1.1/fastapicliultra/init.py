import os
import subprocess
import click
import logging
import shutil


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_REPO_URL = "https://github.com/XmyKhnnt/full-stack-fastapi-template"


def is_git_installed() -> bool:
    """Check if Git is installed."""
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False


def clone_repository(repo_url: str, target_dir: str) -> None:
    """Clone a Git repository."""
    if os.path.exists(target_dir):
        logger.error(f"Target directory '{target_dir}' already exists.")
        raise FileExistsError(f"Directory '{target_dir}' already exists.")

    subprocess.run(["git", "clone", repo_url, target_dir], check=True)
    logger.info(f"Repository cloned successfully into '{target_dir}'.")


@click.command()
@click.option("--repo-url", default=DEFAULT_REPO_URL, help="The URL of the repository to clone.")
@click.option("--target-dir", default="app", help="The target directory to clone into.")
def init(repo_url: str, target_dir: str) -> None:
    """Initialize FastAPI Ultra."""
    click.echo("Initializing FastAPI Ultra...")

    if not is_git_installed():
        click.echo("Error: Git is not installed or not found in PATH.")
        return

    try:
        click.echo(f"Cloning repository from '{repo_url}' into '{target_dir}'...")
        clone_repository(repo_url, target_dir)
        click.echo("Initialization complete.")
    except FileExistsError as e:
        click.echo(f"Error: {e}")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error cloning repository: {e}")
    except Exception as e:
        click.echo(f"Unexpected error: {e}")


if __name__ == "__main__":
    init()
