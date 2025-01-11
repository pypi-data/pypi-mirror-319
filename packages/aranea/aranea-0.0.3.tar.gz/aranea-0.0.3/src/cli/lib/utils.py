"""Utility functions for the CLI."""

import logging
import os
import platform
import subprocess  # nosec B404 - See description below
import sys
from pathlib import Path
from xml.etree.ElementTree import ElementTree  # nosec B405 - no xml parsing

from aranea.g2d.transform_graph_collection_to_mx_file import \
    transform_graph_collection_to_mx_file
from aranea.models.graph_model import GraphCollection
from aranea.models.style_config_model import StyleConfig
from aranea.models.xml_model import MxFile

logger: logging.Logger = logging.getLogger(__name__)


def graph_collection_to_drawio_file(
    graph_collection: GraphCollection, style_config: StyleConfig, path: str
) -> None:
    """Export a GraphCollection to a DrawIO file.

    :param graph_collection: The GraphCollection to export.
    :type graph_collection: GraphCollection
    :param style_config: The StyleConfig to use for the export.
    :type style_config: StyleConfig
    :param path: The path to the output file.
    :type path: str
    """

    mx_file: MxFile = transform_graph_collection_to_mx_file(graph_collection, style_config)
    xml_tree: ElementTree = ElementTree(mx_file.to_xml_tree())  # pyright: ignore
    xml_tree.write(path)
    logger.info("The DrawIO file was exported to %s", path)


def graph_collection_to_json_file(graph_collection: GraphCollection, path: str) -> None:
    """Export a GraphCollection to a JSON file.

    :param graph_collection: The GraphCollection to export.
    :type graph_collection: GraphCollection
    :param path: The path to the output file.
    :type path: str
    """

    graph_collection_json: str = graph_collection.model_dump_json()
    with open(path, "w", encoding="UTF-8") as file:
        file.write(graph_collection_json)
    logger.debug("The JSON model was exported to %s", path)


def export_drawio_file(
    drawio_path: str,
    drawio_file_path: str,
    export_format: str,
    output_dir: str,
    output_file_name: str,
) -> None:
    """Export a DrawIO file to a specified format.

    :param drawio_path: The path to the DrawIO executable.
    :type drawio_path: str
    :param drawio_file_path: The path to the DrawIO file.
    :type drawio_file_path: str
    :param export_format: The format to export the DrawIO file to.
    :type export_format: str
    :param output_dir: The output directory.
    :type output_dir: str
    :param output_file_name: The output file name.
    :type output_file_name: str
    """
    if not Path(drawio_path).is_file():
        logger.error(
            "Can't find a DrawIO executable at %s. Please provide a valid path.", drawio_path
        )
        sys.exit(1)
    else:
        command: list[str] = [
            drawio_path,
            "-x",
            "-f",
            export_format,
            "-o",
            os.path.join(output_dir, output_file_name + "." + export_format),
            drawio_file_path,
            "--disable-dev-shm-usage",
        ]

        # Add --no-sandbox for Linux when running as root
        if platform.system() == "Linux" and os.geteuid() == 0:
            command.insert(1, "--no-sandbox")
            logger.warning("Running DrawIO with --no-sandbox.")
            if os.getenv("CI") == "true":
                logger.debug("Running DrawIO with xvfb-run.")
                command.insert(0, "xvfb-run")

        try:
            logger.debug("Calling: %s", " ".join(command))
            result = subprocess.run(
                command, check=True, text=True, capture_output=True
            )  # nosec B603 - We are aware of possible security implications
            # The user is responsible for the drawio_path,
            # we can't ensure that the path to the exeutable is secure
            logger.debug("DrawIO stdout: %s", result.stdout)
            logger.debug("DrawIO returncode: %s", result.returncode)
            logger.debug("DrawIO stderr: %s", result.stderr)
        except subprocess.CalledProcessError as e:
            logger.error("An error occurred while executing the drawio export: %s", e.stderr)
            sys.exit(1)
