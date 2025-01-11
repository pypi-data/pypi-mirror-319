"""The main entry point for the CLI application of aranea."""

import logging
from pathlib import Path

import click

from cli.create_config import create_config
from cli.json_to_drawio import json_to_drawio
from cli.lib.config import EPILOG, Config
from cli.run import run

_CONTEXT_SETTINGS: dict[str, list[str]] = {"help_option_names": ["-h", "--help"]}
logger: logging.Logger = logging.getLogger(__name__)
root_logger: logging.Logger = logging.getLogger()
_LOGGER_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
logging.basicConfig(
    level=logging.WARNING,
    format=_LOGGER_FORMAT,
)


@click.group(context_settings=_CONTEXT_SETTINGS, epilog=EPILOG)
@click.version_option(package_name="aranea")
@click.option(
    "-c",
    "--config-file",
    "config_file_path",
    default="./pyproject.toml",
    show_default=True,
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    help="Path to the configuration file.",
)
@click.option(
    "-l",
    "--log-level",
    "log_level",
    type=click.Choice(
        ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=True
    ),
    help="Set the log level regarding to the python logging module. Note: If the log level is set\
 in the config file, it is only set after the config file has been passed.  [default: WARNING]",
)
@click.option(
    "-o",
    "--output-dir",
    "output_dir",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        path_type=Path,
    ),
    help="Path to the output directory where aranea can provide you with artefacts. You need to \
ensure that the directory exists.  [default: ./]",
)
@click.option(
    "-d",
    "--drawio-path",
    "drawio_path",
    required=False,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
        executable=True,
    ),
    help="The path to the drawio executable. A path is required to export the architecture to a\
 image like a png. If DrawIO is installed on Linux, aranea detects the path automatically.\
 If you using Windows or macOS, you have to set the path manually.",
)
@click.pass_context
def cli(
    ctx: click.Context,
    config_file_path: Path,
    log_level: str | None,
    output_dir: Path | None,
    drawio_path: Path | None,
) -> None:
    """The main entry point for the CLI application of aranea."""
    if log_level is not None:
        root_logger.setLevel(log_level)

    logger.debug("---Starting the aranea CLI---")

    ctx.obj = Config(config_file_path=config_file_path)

    if ctx.obj.user_config is not None:
        if log_level is not None:
            ctx.obj.user_config["log_level"] = log_level
        if output_dir is not None:
            ctx.obj.user_config["output_dir"] = str(output_dir)
        if drawio_path is not None:
            ctx.obj.user_config["drawio_path"] = str(drawio_path)
    else:
        raise click.ClickException("The user_config needs to be set.")

    root_logger.setLevel(str(ctx.obj.user_config["log_level"]))


cli.add_command(create_config)
cli.add_command(run)
cli.add_command(json_to_drawio)
