"""Module for enriching the graph."""

import fnmatch
import logging
from enum import Enum
from pathlib import Path
from typing import Optional, cast

import pandas as pd

from aranea.models.graph_model import (ComponentNode, EcuClassification,
                                       GraphCollection, TechnicalCapability)

logger = logging.getLogger(__name__)


class ExcelColumnNames(Enum):
    """Column names of the Excel file containing the ECU ratings."""

    ECU_NAME = "ECU Name"
    SECURITY_CLASS = "Security Class"
    EXTERNAL_INTERFACE = "External Interface"
    GATEWAY = "GW"
    LIN_SLAVE = "Lin-Slave"
    DOMAIN = "Domain"


class GraphCollectionEnricher:
    """Class for enriching the GraphCollection with ratings from Excel files."""

    def __init__(self, graph_collection: GraphCollection) -> None:
        """Constructor for the GraphCollectionEnricher class."""
        self.graph_collection: GraphCollection = graph_collection

    def to_bool(self, value: str) -> bool:
        """Checks if a string starts with a 'y' or 'Y'.

        :param value: The string to check.
        :type value: str
        :return: True if the string starts with 'y' or 'Y', otherwise False.
        :rtype: bool
        """
        return value.strip().lower().startswith("y")

    def read_ecu_ratings(self, excel_file_path: Path) -> pd.DataFrame:
        """Converts the ECU ratings from an Excel file to a DataFrame.

        Duplicated rows in the Excel file will be removed.

        :param excel_file_path: The path to the Excel file containing the ECU ratings.
        :type excel_file_path: Path
        :return: The DataFrame containing the ECU ratings.
        :rtype: pd.DataFrame
        """
        # write excel file to DataFrame
        df: pd.DataFrame = pd.read_excel(  # pyright: ignore
            io=excel_file_path,
            sheet_name=0,
            header=0,
            index_col=None,
            dtype={
                ExcelColumnNames.ECU_NAME.value: str,
                ExcelColumnNames.SECURITY_CLASS.value: pd.UInt8Dtype(),
                ExcelColumnNames.EXTERNAL_INTERFACE.value: pd.StringDtype(),
                ExcelColumnNames.GATEWAY.value: pd.StringDtype(),
                ExcelColumnNames.LIN_SLAVE.value: pd.StringDtype(),
                ExcelColumnNames.DOMAIN.value: pd.StringDtype(),
            },
            engine="openpyxl",
        )

        # convert yes/no columns to bool
        yes_no_columns: list[str] = [
            ExcelColumnNames.EXTERNAL_INTERFACE.value,
            ExcelColumnNames.GATEWAY.value,
            ExcelColumnNames.LIN_SLAVE.value,
        ]
        for col in yes_no_columns:
            df[col] = df[col].apply(self.to_bool)  # pyright: ignore

        df = df.drop_duplicates(keep="first")
        # set the unique ECU name as the index of the DataFrame
        df.set_index(ExcelColumnNames.ECU_NAME.value, inplace=True)  # pyright: ignore

        logger.info("Imported the ECU ratings from: %s", excel_file_path)
        logger.debug("Imported ratings: \n%s", df)

        return df

    def find_ecu_pattern(self, ecu_name: str, ratings: pd.DataFrame) -> str | None:
        """Finds the pattern in the DataFrame that matches the ECU name.

        :param ecu_name: The name of the ECU.
        :type ecu_name: str
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :return: The pattern that matches the ECU name.
        :rtype: str | None
        """
        patterns: list[str] = []
        pattern: str | None = None

        # safe all patterns that match the ECU name
        for index, _ in ratings.iterrows():  # pyright: ignore
            ecu_pattern = str(index)
            if fnmatch.fnmatch(ecu_name, ecu_pattern):
                patterns.append(ecu_pattern)

        # return None or the longest pattern
        if len(patterns) == 0:
            logger.warning(
                "Found no rating for ECU '%s'.",
                ecu_name,
            )
        else:
            patterns = sorted(patterns, key=len, reverse=True)
            logger.debug(
                "Found %s patterns %s for ECU '%s'.",
                str(len(patterns)),
                str(patterns),
                ecu_name,
            )
            if len(patterns) > 1:
                logger.debug("Using the longest match: '%s'.", str(patterns[0]))
            pattern = patterns[0]

        return pattern

    def __set_security_class(
        self, node: ComponentNode, ratings: pd.DataFrame, pattern: str
    ) -> None:
        """Overwrites the security class of the ComponentNode based on the ratings DataFrame.

        :param node: The node to set the security class for.
        :type node: ComponentNode
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :param pattern: The pattern that matches the ECU name of the node.
        :type pattern: str
        """
        security_class: int | None = cast(
            Optional[int],
            ratings.at[pattern, ExcelColumnNames.SECURITY_CLASS.value],  # pyright: ignore
        )
        if not pd.isna(security_class):
            node.security_class = int(security_class)
        else:
            node.security_class = None

    def __set_external_interface(
        self, node: ComponentNode, ratings: pd.DataFrame, pattern: str
    ) -> None:
        """Sets or removes the EXTERNAL_INTERFACE classification of the ComponentNode
        based on the ratings DataFrame.

        :param node: The node to set the EXTERNAL_INTERFACE classification for.
        :type node: ComponentNode
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :param pattern: The pattern that matches the ECU name of the node.
        :type pattern: str
        """
        if ratings.at[pattern, ExcelColumnNames.EXTERNAL_INTERFACE.value]:  # pyright: ignore
            node.classifications.add(EcuClassification.EXTERNAL_INTERFACE)
        else:
            node.classifications.discard(EcuClassification.EXTERNAL_INTERFACE)

    def __set_lin_connected_ecu(
        self, node: ComponentNode, ratings: pd.DataFrame, pattern: str
    ) -> None:
        """Sets or removes the LIN_CONNECTED_ECU classification of the ComponentNode
        based on the ratings DataFrame.

        The LIN_CONNECTED_ECU classification should normally already be set during the
        PDF parsing process (g2d). This method will print a warning if the GraphCollection
        and the Excel file do not match. The classification will be set according to the
        Excel file.

        :param node: The node to set the LIN_CONNECTED_ECU classification for.
        :type node: ComponentNode
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :param pattern: The pattern that matches the ECU name of the node.
        :type pattern: str
        """
        lin_connected_excel: bool = ratings.at[  # pyright: ignore
            pattern, ExcelColumnNames.LIN_SLAVE.value
        ]
        lin_connected_node: bool = EcuClassification.LIN_CONNECTED_ECU in node.classifications

        if lin_connected_node != lin_connected_excel:
            logger.warning(
                "Mismatch between the GraphCollection (from PDF) and Excel for LIN_CONNECTED_ECU "
                "classification for ECU '%s'.\n"
                "Classification 'LIN_CONNECTED_ECU' according to Excel: %s. (will be used)\n"
                "Classification 'LIN_CONNECTED_ECU' according to GraphCollection (from PDF): %s",
                (
                    node.innerText[0]
                    if node.innerText is not None
                    else node.outerText[0]  # type: ignore
                ),  # type ignore because outer text is how we match, can't be None
                str(lin_connected_excel),  # pyright: ignore
                str(lin_connected_node),
            )

        if lin_connected_excel:
            node.classifications.add(EcuClassification.LIN_CONNECTED_ECU)
        else:
            node.classifications.discard(EcuClassification.LIN_CONNECTED_ECU)

    def __set_gateway(self, node: ComponentNode, ratings: pd.DataFrame, pattern: str) -> None:
        """Sets the gateway classification of the ComponentNode based on the ratings DataFrame.

        :param node: The node to set the gateway classification for.
        :type node: ComponentNode
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :param pattern: The pattern that matches the ECU name of the node.
        :type pattern: str
        """
        domain: str | None = cast(
            Optional[str], ratings.at[pattern, ExcelColumnNames.DOMAIN.value]  # pyright: ignore
        )
        if (
            not pd.isna(domain)
            and ratings.at[pattern, ExcelColumnNames.GATEWAY.value]  # pyright: ignore
        ):
            node.classifications.discard(EcuClassification.NON_DOMAIN_GATEWAY)
            node.classifications.add(EcuClassification.DOMAIN_GATEWAY)
        elif ratings.at[pattern, ExcelColumnNames.GATEWAY.value]:  # pyright: ignore
            node.classifications.discard(EcuClassification.DOMAIN_GATEWAY)
            node.classifications.add(EcuClassification.NON_DOMAIN_GATEWAY)
        else:
            node.classifications.discard(EcuClassification.DOMAIN_GATEWAY)
            node.classifications.discard(EcuClassification.NON_DOMAIN_GATEWAY)

    def set_node_attributes(self, node: ComponentNode, ratings: pd.DataFrame, pattern: str) -> None:
        """Sets the attributes of the node based on the ratings DataFrame.

        :param node: The node to set the attributes for.
        :type node: ComponentNode
        :param ratings: The DataFrame containing the ECU ratings.
        :type ratings: pd.DataFrame
        :param pattern: The pattern that matches the ECU name of the node.
        :type pattern: str
        """
        self.__set_security_class(node, ratings, pattern)
        self.__set_external_interface(node, ratings, pattern)
        self.__set_lin_connected_ecu(node, ratings, pattern)
        self.__set_gateway(node, ratings, pattern)

    def enrich_technical_capabilities(
        self, node: ComponentNode, technical_capabilities: list[TechnicalCapability]
    ) -> None:
        """Overwrites the technical capabilities values of a node.

        Only for the TechnicalCapability the node already has.

        :param node: The ComponentNode to enrich.
        :type node: ComponentNode
        :param technical_capabilities: The technical capabilities to possible enrich the node with.
        :type technical_capabilities: list[TechnicalCapability]
        :return: The enriched ComponentNode.
        :rtype: ComponentNode
        """

        for cap in technical_capabilities:
            for node_cap in node.technical_capabilities:
                if node_cap.name == cap.name:
                    node_cap.attack_potential = cap.attack_potential
                    node_cap.feasibility_rating = cap.feasibility_rating

    def enrich(
        self, excel_file_path: Path, technical_capabilities: list[TechnicalCapability]
    ) -> GraphCollection:
        """Reads the ECU ratings from an Excel file and the technical capabilities
        to enriches the graph with them.

        If a node has an 'outerText' attribute, the ECU name is extracted from it.
        The ECU name is then matched with the ratings DataFrame and
        the attributes of the node are set accordingly.
        If a ComponentNode has a technical capability, the technical capability values are updated.

        :param excel_file_path: The path to the Excel file containing the ECU ratings.
        :type excel_file_path: Path
        :param technical_capabilities: The technical capabilities to enrich the graph with.
        :type technical_capabilities: list[TechnicalCapability]
        :return: The enriched graph.
        :rtype: Graph
        """
        ratings: pd.DataFrame = self.read_ecu_ratings(excel_file_path)

        for graph in self.graph_collection.graphs:
            for node in graph.nodes.values():
                if not isinstance(node, ComponentNode):
                    continue

                if node.outerText is None:
                    logger.info("The 'outerText' of Node is 'None': %s", str(node))
                    logger.info("Can't look for a matching ECU in the ratings")
                    continue
                ecu_name: str = node.outerText[0]
                pattern: str | None = self.find_ecu_pattern(ecu_name, ratings)
                if pattern is None:
                    continue

                self.set_node_attributes(node, ratings, pattern)
                self.enrich_technical_capabilities(node, technical_capabilities)

        GraphCollection.model_validate(self.graph_collection)

        return self.graph_collection
