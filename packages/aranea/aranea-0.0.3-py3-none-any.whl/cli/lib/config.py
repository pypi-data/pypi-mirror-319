"""Module for the configuration class of CLI configuration."""

import json
import logging
import shutil
from pathlib import Path
from typing import Any, TypedDict, cast

import click

from aranea.g2d.style_configs.get_default_style_config import \
    get_default_style_config
from aranea.models.graph_model import (TechnicalCapability,
                                       TechnicalCapabilityNames)
from aranea.models.style_config_model import StyleConfig
from aranea.p2g import parse_page
from cli.lib.toml_tools import aranea_config_available, parse_toml

logger: logging.Logger = logging.getLogger(__name__)

EPILOG: str = "Docs: https://674c8e49-0742-43e3-bf6f-def680a9d585.ul.bw-cloud-instance.org"


class TechnicalCapabilityDict(TypedDict):
    """Type definition for the technical capability dictionary.

    Should be similar to the TechnicalCapability model.
    """

    name: str
    attack_potential: int
    feasibility_rating: int


class DefaultConfig(TypedDict):
    """Type definition for the default configuration of Aranea.

    Containing the StyleConfig as a dict.
    """

    output_dir: str
    drawio_path: str
    log_level: str
    p2g: dict[str, Any]
    g2d: dict[str, Any]
    ge: list[TechnicalCapabilityDict]


class UserConfig(TypedDict):
    """Type definition for the user configuration of Aranea."""

    output_dir: str
    drawio_path: str
    log_level: str
    p2g: dict[str, Any]
    g2d: StyleConfig
    ge: list[TechnicalCapability]


class Config:
    """Configuration class containing configuration settings for other commands."""

    @staticmethod
    def get_default_technical_capability() -> list[TechnicalCapabilityDict]:
        """Return the default technical capabilities as a list of dictionaries.

        :return: The default technical capabilities.
        :rtype: list[dict[str, str | int]]
        """
        technical_capabilities: list[TechnicalCapabilityDict] = []
        for capability in TechnicalCapabilityNames:
            technical_capability = TechnicalCapability(name=capability)
            technical_capabilities.append(json.loads(technical_capability.model_dump_json()))

        return technical_capabilities

    default_config: DefaultConfig = {
        "output_dir": "./",
        "drawio_path": shutil.which("drawio") or "/path/to/draw.io",
        "log_level": "WARNING",
        "p2g": parse_page.__kwdefaults__,
        "g2d": json.loads(get_default_style_config().model_dump_json()),
        "ge": get_default_technical_capability(),
    }
    toml_config: dict[str, Any]
    user_config: UserConfig

    def __init__(self, config_file_path: Path) -> None:
        """Constructor for the Config class."""

        if config_file_path.exists() and aranea_config_available(config_file_path):
            logger.info("Reading the config from %s", config_file_path)
            config_file: dict[str, Any] = parse_toml(config_file_path)

            if "tool" in config_file and "aranea" in config_file["tool"]:
                self.toml_config = config_file["tool"]["aranea"]

                logger.debug("Overwriting the default values with the user values.")
                merged_config: DefaultConfig = cast(
                    DefaultConfig,
                    self.merge_dicts(cast(dict[str, Any], self.default_config), self.toml_config),
                )

                self.user_config = UserConfig(
                    output_dir=merged_config["output_dir"],
                    drawio_path=merged_config["drawio_path"],
                    log_level=merged_config["log_level"],
                    p2g=merged_config["p2g"],
                    g2d=StyleConfig.model_validate(merged_config["g2d"]),
                    ge=self.validate_technical_capabilities(merged_config["ge"]),
                )

            else:
                logger.info("No Aranea config found in %s", str(config_file_path))

        else:
            logger.info("No config found for %s", str(config_file_path))
            logger.info("Using the default config.")

            tmp_config = cast(dict[str, Any], self.default_config.copy())
            tmp_config["g2d"] = StyleConfig.model_validate(tmp_config["g2d"])

            self.user_config = cast(UserConfig, tmp_config.copy())

    def validate_technical_capabilities(
        self, technical_capabilities: list[TechnicalCapabilityDict]
    ) -> list[TechnicalCapability]:
        """Convertes the technical capabilities from the config to a list of TechnicalCapability.

        It checks if the technical capabilities are valid and if not, raises an error.

        :param technical_capabilities: The technical capabilities from the config.
        :type technical_capabilities: list[dict[str, str | int]]
        :return: The list of TechnicalCapability.
        :rtype: list[TechnicalCapability]
        """

        capabilities: list[TechnicalCapability] = []

        for cap in technical_capabilities:
            try:
                capability = TechnicalCapability(
                    name=TechnicalCapabilityNames(cap["name"]),
                    attack_potential=cap.get(
                        "attack_potential",
                        TechnicalCapability.model_fields["attack_potential"].default,
                    ),
                    feasibility_rating=cap.get(
                        "feasibility_rating",
                        TechnicalCapability.model_fields["feasibility_rating"].default,
                    ),
                )
                capabilities.append(capability)
            except KeyError as e:
                raise KeyError(f"Missing required field: {e}") from e
            except ValueError as e:
                raise ValueError(f"Validation error: {e}") from e

        return capabilities

    def merge_dicts(self, dict_a: dict[str, Any], dict_b: dict[str, Any]) -> dict[str, Any]:
        """Merge two dictionaries.

        The dict_a is the base dictionary. If a key from dict_a is also in dict_b,
        the value of dict_b is used. New keys from dict_b will not be added to dict_a.
        The function returns a new dictionary. Nested dictionaries are also merged.

        :param dict_a: The base dictionary.
        :type dict_a: dict[str, Any]
        :param dict_b: The dictionary with the new values.
        :type dict_b: dict[str, Any]
        :return: The new merged dictionary.
        :rtype: dict[str, Any]
        """
        merged: dict[str, Any] = dict_a.copy()
        for key, value in dict_a.items():
            if key in dict_b:
                if isinstance(value, dict) and isinstance(dict_b[key], dict):
                    # Recursively merge nested dictionaries
                    merged[key] = self.merge_dicts(cast(dict[str, Any], value), dict_b[key])
                else:
                    merged[key] = dict_b[key]
        return merged

    def print_config(self) -> None:
        """Print the default configuration of Aranea to the terminal."""
        click.secho("The default configuration is:")
        click.secho(json.dumps(self.default_config, indent=4))
