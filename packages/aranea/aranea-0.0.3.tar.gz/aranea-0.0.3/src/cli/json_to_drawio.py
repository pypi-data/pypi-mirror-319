"""Module for creating a DrawIO file from a Aranea JSON file."""

import logging
import os
from pathlib import Path

import click

from aranea.models.graph_model import GraphCollection
from cli.lib.config import EPILOG, Config
from cli.lib.utils import export_drawio_file, graph_collection_to_drawio_file

logger: logging.Logger = logging.getLogger(__name__)


@click.command(epilog=EPILOG)
@click.argument(
    "architecture_json_path",
    nargs=1,
    required=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
)
@click.option(
    "-f",
    "--export-format",
    "export_format",
    type=click.Choice(["pdf", "png", "jpg", "svg", "vsdx", "xml"], case_sensitive=True),
    help="If set, the detected architecture is exported to the specified format. The export will\
 be disabled if the drawio_path is not set or the '--no-drawio-file' flag is set.\
 If you are using ``--export-format`` under Linux and EUID is 0 (root), drawio will be\
 run with ``--no-sandbox``. If the environment variable ``CI`` is also set to ``true`` it will\
 be run with ``xvfb-run``. This requires that ``xvfb`` is installed on the system.",
)
@click.option(
    "-n",
    "--output-file-name",
    "output_file_name",
    default="aranea_result",
    show_default=True,
    type=str,
    help="You can specify a custom name for the output file.",
)
@click.pass_obj
def json_to_drawio(
    config: Config,
    architecture_json_path: Path,
    export_format: str | None,
    output_file_name: str,
) -> None:
    """Creates a DrawIO file from a JSON file.

    The provided JSON file must be a valid Aranea ``GraphCollection``.
    """

    logger.debug("---Starting the json-to-drawio command---")

    with open(architecture_json_path, "r", encoding="UTF-8") as f:
        graph_collection: GraphCollection = GraphCollection.model_validate_json(f.read())
    drawio_file_path: str = os.path.join(
        config.user_config["output_dir"], output_file_name + ".drawio"
    )
    graph_collection_to_drawio_file(
        graph_collection,
        config.user_config["g2d"],
        drawio_file_path,
    )

    if export_format is not None:
        export_drawio_file(
            drawio_path=config.user_config["drawio_path"],
            drawio_file_path=drawio_file_path,
            export_format=export_format,
            output_dir=config.user_config["output_dir"],
            output_file_name=output_file_name,
        )
