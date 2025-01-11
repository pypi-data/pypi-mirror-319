from importlib.metadata import version

import click
import uvicorn


@click.command()
@click.option(
    "--host", default="127.0.0.1", show_default=True, help="Bind socket to this host."
)
@click.option(
    "--port",
    default=8000,
    show_default=True,
    help="Bind socket to this port. If 0, an available port will be picked.",
)
@click.option("--uds", help="Bind to a UNIX domain socket.")
@click.option(
    "--workers",
    help=(
        "Number of worker processes. "
        "Defaults to the $WEB_CONCURRENCY environment variable if available, or 1."
    ),
    type=int,
)
@click.version_option(version("pssecret_server"))
def cli(**kwargs) -> None:
    uvicorn.run("pssecret_server.main:app", **kwargs)
