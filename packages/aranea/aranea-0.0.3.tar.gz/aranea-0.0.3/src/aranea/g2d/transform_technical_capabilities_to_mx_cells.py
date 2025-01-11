"""
This module provides a model transformation (Graph-Model->XML-Model) for
icons associated with technical capabilities of a ComponentNode.
"""

import logging
from typing import Literal, Self, cast

from aranea.models.custom_xml_shapes.icons import IconFactory, IconIdentifier
from aranea.models.graph_model import (ComponentNode, TechnicalCapability,
                                       TechnicalCapabilityNames)
from aranea.models.xml_model import (MxCellShape, MxCellStyle,
                                     MxCellStyleDefaultShape, MxGeometryShape)

DEFAULT_ICON_DIMENSION_FACTOR = 2
logger = logging.getLogger(__name__)


def get_technical_capability_icon_str(
    technical_capability: TechnicalCapability | Literal["AMG_ONLY"],
) -> str | None:
    """
    Function for mapping a technical capability
    to the respective icon.

    :param technical_capability: The technical capability
    :type technical_capability: TechnicalCapability
    :return: The respective icon string.
    :rtype: str
    """
    icon_factory: IconFactory = IconFactory()

    if isinstance(technical_capability, str) and "AMG_ONLY" == technical_capability:
        return str(icon_factory.get_icon_str(IconIdentifier.AMG))
    if not isinstance(technical_capability, TechnicalCapability):
        raise ValueError(f"Unknown technical capability: {technical_capability}")

    match technical_capability.name:
        case TechnicalCapabilityNames.NETWORK_SWITCH:
            return str(icon_factory.get_icon_str(IconIdentifier.NETWORK_SWITCH))
        case TechnicalCapabilityNames.BACKEND:
            return str(icon_factory.get_icon_str(IconIdentifier.BACKEND))
        case TechnicalCapabilityNames.CELLULAR:
            return str(icon_factory.get_icon_str(IconIdentifier.CELLULAR))
        case TechnicalCapabilityNames.WIFI:
            return str(icon_factory.get_icon_str(IconIdentifier.WIFI))
        case TechnicalCapabilityNames.BLUETOOTH:
            return str(icon_factory.get_icon_str(IconIdentifier.BLUETOOTH))
        case TechnicalCapabilityNames.USB:
            return str(icon_factory.get_icon_str(IconIdentifier.USB))
        case TechnicalCapabilityNames.SATELLITE:
            return str(icon_factory.get_icon_str(IconIdentifier.SATELLITE))
        case TechnicalCapabilityNames.CAR_CHARGER:
            return str(icon_factory.get_icon_str(IconIdentifier.CAR_CHARGER))
        case TechnicalCapabilityNames.DIGITAL_BROADCAST:
            return str(icon_factory.get_icon_str(IconIdentifier.DIGITAL_BROADCAST))
        case TechnicalCapabilityNames.ANALOG_BROADCAST:
            return str(icon_factory.get_icon_str(IconIdentifier.ANALOG_BROADCAST))
        case TechnicalCapabilityNames.NFC:
            return str(icon_factory.get_icon_str(IconIdentifier.NFC))
        case _:
            logger.debug("For %s is no icon defined!", technical_capability.name)
            return None


class IconPositioner:
    """
    Class for generating icon positions below a ComponentNode.
    """

    def __init__(
        self,
        component_node: ComponentNode,
        rem_size: float,
    ):
        self.x = component_node.xRemFactor * rem_size
        self.y = component_node.yRemFactor * rem_size
        self.width = component_node.widthRemFactor * rem_size
        self.height = component_node.heightRemFactor * rem_size
        self.step_x = rem_size * DEFAULT_ICON_DIMENSION_FACTOR
        self.step_y = rem_size * DEFAULT_ICON_DIMENSION_FACTOR
        self.current_x = self.x
        self.current_y = self.y + self.height
        self.is_initial_position = True

    def reset(self) -> Self:
        """
        Function for resetting the position generation.
        """
        self.current_x = self.x
        self.current_y = self.y + self.height
        self.is_initial_position = True

        return self

    def get_next_position(self) -> tuple[float, float]:
        """
        Function for getting the next icon position.
        Wraps around when icons exceed width of node.

        :return: A tuple of x and y coordinates.
        :rtype: tuple[float, float]
        """
        if self.is_initial_position:
            self.is_initial_position = False
            return self.current_x, self.current_y

        self.current_x += self.step_x

        if self.current_x + self.step_x > self.width + self.x:
            self.current_x = self.x
            self.current_y += self.step_y

        return self.current_x, self.current_y


def transform_technical_capabilities_to_mx_cells(
    component_node: ComponentNode, rem_size: float
) -> list[MxCellShape]:
    """
    Function for generating MxCells for a ComponentNode's
    technical capabilities.

    :param component_node: The component node.
    :type component_node: ComponentNode
    :param rem_size: The size of the root element.
    :type rem_size: float
    :return: The MxCells of the technical capability icons.
    :rtype: list[MxCellShape]
    """
    mx_cells: list[MxCellShape] = []
    icon_positioner: IconPositioner = IconPositioner(component_node, rem_size)

    technical_capabilities: set[TechnicalCapability | Literal["AMG_ONLY"]] = cast(
        set[TechnicalCapability | Literal["AMG_ONLY"]], component_node.technical_capabilities
    )

    if component_node.amg_only:
        technical_capabilities |= {"AMG_ONLY"}

    for technical_capability in component_node.technical_capabilities:
        icon_position = icon_positioner.get_next_position()

        mx_cells.append(
            MxCellShape(
                attr_style=MxCellStyle(
                    shape=MxCellStyleDefaultShape.IMAGE,
                    image=get_technical_capability_icon_str(technical_capability),
                ).to_semicolon_string(),
                geometry=MxGeometryShape(
                    attr_x=icon_position[0],
                    attr_y=icon_position[1],
                    attr_height=rem_size * DEFAULT_ICON_DIMENSION_FACTOR,
                    attr_width=rem_size * DEFAULT_ICON_DIMENSION_FACTOR,
                ),
            )
        )

    return mx_cells
