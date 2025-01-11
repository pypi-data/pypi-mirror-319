import os
import click
import sys
from preswald.server import start_server
from preswald.logging import configure_logging
from preswald.deploy import deploy as deploy_app, stop as stop_app


@click.group()
def cli():
    """
    Preswald CLI - A lightweight framework for interactive data apps.
    """
    pass


@cli.command()
@click.argument("name", default="preswald_project")
def init(name):
    """
    Initialize a new Preswald project.

    This creates a directory with boilerplate files like `hello.py` and `config.toml`.
    """
    try:
        os.makedirs(name, exist_ok=True)
        os.makedirs(os.path.join(name, "images"), exist_ok=True)

        # Copy default branding files from package resources
        import pkg_resources
        import shutil

        # Copy default branding files
        default_static_dir = pkg_resources.resource_filename("preswald", "static")
        default_favicon = os.path.join(default_static_dir, "favicon.ico")
        default_logo = os.path.join(default_static_dir, "logo.png")

        # Copy to project's images directory
        shutil.copy2(default_favicon, os.path.join(name, "images", "favicon.ico"))
        shutil.copy2(default_logo, os.path.join(name, "images", "logo.png"))

        # Create boilerplate files
        with open(os.path.join(name, "hello.py"), "w") as f:
            f.write(
                """from preswald import text, connect, view

# Connect to data sources
# You can use the config.toml file to configure your connections
# or connect directly using the source parameter:

# Example connections:
# db = connect(source="postgresql://user:pass@localhost:5432/dbname")
# csv_data = connect(source="data/file.csv")
# json_data = connect(source="https://api.example.com/data.json")

# Or use the configuration from config.toml:
# db = connect()  # Uses the default_source from config.toml

text("# Welcome to Preswald!")
text("This is your first app. 🎉")

# Example: View data from a connection
# view("connection_name", limit=50)
"""
            )

        with open(os.path.join(name, "config.toml"), "w") as f:
            f.write(
                """[project]
title = "Preswald Project"
version = "0.1.0"
port = 8501

[branding]
name = "Preswald Project"
logo = "images/logo.png"
favicon = "images/favicon.ico"

[theme.color]
primary = "#4CAF50"
secondary = "#FFC107"
background = "#FFFFFF"
text = "#000000"

[theme.font]
family = "Arial, sans-serif"
size = "16px"

[data]
default_source = "postgres"   # Default data source. Options: "csv", "postgres", "mysql", "json", "parquet"
cache = true                  # Enable caching of data

[data.postgres]
host = "localhost"            # PostgreSQL host
port = 5432                   # PostgreSQL port
dbname = "mydb"              # Database name
user = "user"                # Username
# password is stored in secrets.toml

[data.mysql]
host = "localhost"           # MySQL host
port = 3306                 # MySQL port
dbname = "mydb"            # Database name
user = "user"              # Username
# password is stored in secrets.toml

[data.csv]
path = "data/sales.csv"    # Path to CSV file

[data.json]
url = "https://api.example.com/data"  # URL for JSON data
# api_key is stored in secrets.toml

[data.parquet]
path = "data/sales.parquet"  # Path to Parquet file
"""
            )

        with open(os.path.join(name, "secrets.toml"), "w") as f:
            f.write(
                """# Add your secrets here (DO NOT commit this file)

[data.postgres]
password = ""  # PostgreSQL password

[data.mysql]
password = ""  # MySQL password

[data.json]
api_key = ""  # API key for JSON endpoint
                    
[logging]
level = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
"""
            )

        with open(os.path.join(name, ".gitignore"), "w") as f:
            f.write("secrets.toml\n")

        with open(os.path.join(name, "README.md"), "w") as f:
            f.write(
                """# Preswald Project

## Setup
1. Configure your data connections in `config.toml`
2. Add sensitive information (passwords, API keys) to `secrets.toml`
3. Run your app with `preswald run hello.py`
"""
            )

        click.echo(f"Initialized a new Preswald project in '{name}/'")
    except Exception as e:
        click.echo(f"Error initializing project: {e}")


@cli.command()
@click.argument("script", default="hello.py")
@click.option("--port", default=8501, help="Port to run the server on.")
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default=None,  # This makes it truly optional
    help="Set the logging level (overrides config file)",
)
def run(script, port, log_level):
    """
    Run a Preswald app.

    By default, it runs the `hello.py` script on localhost:8501.
    """
    if not os.path.exists(script):
        click.echo(f"Error: Script '{script}' not found.")
        return

    config_path = os.path.join(os.path.dirname(script), "config.toml")
    log_level = configure_logging(config_path=config_path, level=log_level)

    click.echo(
        f"Running '{script}' on http://localhost:{port} with log level {log_level}"
    )
    start_server(script=script, port=port)


@cli.command()
@click.argument("script", default="app.py")
@click.option(
    "--platform",
    type=click.Choice(
        ["local", "cloud-run", "aws"], case_sensitive=False
    ),
    default="local",
    help="Platform for deployment.",
)
@click.option("--port", default=8501, help="Port for deployment.")
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default=None,  # This makes it truly optional
    help="Set the logging level (overrides config file)",
)
def deploy(script, platform, port, log_level):
    """
    Deploy your Preswald app locally.

    This allows you to share the app within your local network.
    """
    try:
        if platform == "aws":
            click.echo(f"\nWe're working on supporting AWS soon! Please enjoy some coffee and bananas in the meantime")
            return

        if not os.path.exists(script):
            click.echo(f"Error: Script '{script}' not found.")
            return

        config_path = os.path.join(os.path.dirname(script), "config.toml")
        log_level = configure_logging(config_path=config_path, level=log_level)

        url = deploy_app(script, platform)
        click.echo(f"\nDeployment successful! 🎉")
        click.echo(f"Your app is running at: {url}")

    except Exception as e:
        click.echo(f"Error deploying app: {e}")


@cli.command()
@click.argument("script", default="app.py")
def stop(script):
    """
    Stop the currently running deployment.

    This command must be run from the same directory as your Preswald app.
    """
    try:
        if not os.path.exists(script):
            click.echo(f"Error: Script '{script}' not found.")
            return
        stop_app(script)
        click.echo("Deployment stopped successfully.")
    except Exception as e:
        click.echo(f"Error stopping deployment: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()  # Ensures the CLI is callable when executed directly
