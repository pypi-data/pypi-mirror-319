"""Module for executing aranea."""

import logging
import os
from pathlib import Path

import click

from aranea.models.graph_model import Graph, GraphCollection
from aranea.p2g import parse_page
from cli.lib.config import EPILOG, Config
from cli.lib.utils import (export_drawio_file, graph_collection_to_drawio_file,
                           graph_collection_to_json_file)

logger: logging.Logger = logging.getLogger(__name__)


@click.command(epilog=EPILOG)
@click.argument(
    "architecture_pdf_path",
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
    "--json-model/--no-json-model",
    "json_model",
    is_flag=True,
    show_default=True,
    default=True,
    required=False,
    type=bool,
    help="If set, the detected architecture is passed as a json file (a GraphCollection) to \
the output folder.",
)
@click.option(
    "--drawio-file/--no-drawio-file",
    "drawio_file",
    is_flag=True,
    show_default=True,
    default=True,
    required=False,
    type=bool,
    help="If set, from the detected architecture a DrawIO file is created and saved to the output\
 folder.",
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
    help="You can specify a custom name for the output files.",
)
@click.pass_obj
def run(
    config: Config,
    architecture_pdf_path: Path,
    json_model: bool,
    output_file_name: str,
    drawio_file: bool,
    export_format: str | None,
) -> None:
    """Run aranea to detect an architecture on a given PDF file."""

    logger.debug("---Starting the run command---")

    logger.debug("Starting the parsing process of the PDF file.")
    graph: Graph = parse_page(
        pdfpath=str(architecture_pdf_path),
        ecu_min_height=config.user_config["p2g"]["ecu_min_height"],
        ecu_max_height=config.user_config["p2g"]["ecu_max_height"],
        xor_min_height=config.user_config["p2g"]["xor_min_height"],
        obd_min_height=config.user_config["p2g"]["obd_min_height"],
        obd_max_height=config.user_config["p2g"]["obd_max_height"],
        obd_min_width=config.user_config["p2g"]["obd_min_width"],
        obd_max_width=config.user_config["p2g"]["obd_max_width"],
        obd_color=config.user_config["p2g"]["obd_color"],
    )
    graph_collection: GraphCollection = GraphCollection(graphs=[graph])

    if json_model:
        json_file_path: str = os.path.join(
            config.user_config["output_dir"], output_file_name + ".json"
        )
        graph_collection_to_json_file(graph_collection, json_file_path)

    if drawio_file:
        drawio_file_path: str = os.path.join(
            config.user_config["output_dir"], output_file_name + ".drawio"
        )
        graph_collection_to_drawio_file(
            graph_collection, config.user_config["g2d"], drawio_file_path
        )

        if export_format is not None:
            export_drawio_file(
                drawio_path=config.user_config["drawio_path"],
                drawio_file_path=drawio_file_path,
                export_format=export_format,
                output_dir=config.user_config["output_dir"],
                output_file_name=output_file_name,
            )
