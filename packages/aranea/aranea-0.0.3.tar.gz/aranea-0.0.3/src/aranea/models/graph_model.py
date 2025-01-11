"""
This module provides the pydantic model for working with graph data.
"""

from __future__ import annotations

from enum import Enum
from typing import Annotated, Any, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import UuidVersion
from shapely import Polygon


class TextOrientation(Enum):
    """Enum for the orientation of the text."""

    VERTICAL = "VERTICAL"
    HORIZONTAL = "HORIZONTAL"


type RemFactor = float
type Text = tuple[str, TextOrientation, RemFactor]


def get_default_text(
    text: str,
    *,
    text_orientation: TextOrientation = TextOrientation.HORIZONTAL,
    rem_factor: RemFactor = 1,
) -> Text:
    """
    Function for creating a default text tuple.

    :param text: The corresponding text
    :type text: str
    :param text_orientation: The orientation of the text
    :type text_orientation: TextOrientation
    :param rem_factor: The rem factor of the text
    :type rem_factor: RemFactor
    :return: The default text tuple
    :rtype: Text
    """
    return text, text_orientation, rem_factor


class NodeType(Enum):
    """Enum for the type of the node."""

    COMPONENT = "COMPONENT"
    XOR = "XOR"
    TEXT = "TEXT"
    WAYPOINT = "WAYPOINT"


class Node(BaseModel):
    """Base class for all nodes."""

    model_config = ConfigDict(extra="forbid")

    type: NodeType
    xRemFactor: RemFactor = Field(
        description="Origin is in upper left corner of the document, x increases to the right. \
Factor orients itself on the respective Root Element Size used in the document.",
    )
    yRemFactor: RemFactor = Field(
        description="Origin is in upper left corner of the document, y increases downwards. \
Factor orients itself on the respective Root Element Size used in the document.",
    )


class TechnicalCapabilityNames(Enum):
    """Enum for the supported technical capabilities."""

    ANALOG_BROADCAST = "ANALOG_BROADCAST"
    BACKEND = "BACKEND"
    BLUETOOTH = "BLUETOOTH"
    CAR_CHARGER = "CAR_CHARGER"
    CELLULAR = "CELLULAR"
    CLOUD = "CLOUD"
    DIGITAL_BROADCAST = "DIGITAL_BROADCAST"
    DVB = "DVB"
    NETWORK_SWITCH = "NETWORK_SWITCH"
    NFC = "NFC"
    OBD = "OBD"
    PLC = "PLC"
    SATELLITE = "SATELLITE"
    USB = "USB"
    UWB = "UWB"
    WIFI = "WIFI"


class TechnicalCapability(BaseModel):
    """Model for the technical capabilities."""

    name: TechnicalCapabilityNames
    attack_potential: int = 0
    feasibility_rating: int = 0

    def __hash__(self) -> int:
        return hash((self.name, self.attack_potential, self.feasibility_rating))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, TechnicalCapability):
            return (
                self.name == other.name
                and self.attack_potential == other.attack_potential
                and self.feasibility_rating == other.feasibility_rating
            )
        return False


class EcuClassification(Enum):
    """Enum for the supported classification of the ECUs."""

    ECU = "ECU"
    NEW_ECU = "NEW_ECU"
    ECU_ONLY_IN_BR = "ECU_ONLY_IN_BR"
    DOMAIN_GATEWAY = "DOMAIN_GATEWAY"
    NON_DOMAIN_GATEWAY = "NON_DOMAIN_GATEWAY"
    LIN_CONNECTED_ECU = "LIN_CONNECTED_ECU"
    ENTRY_POINT = "ENTRY_POINT"
    CRITICAL_ELEMENT = "CRITICAL_ELEMENT"
    EXTERNAL_INTERFACE = "EXTERNAL_INTERFACE"


class ComponentNode(Node):
    """Model for the component nodes."""

    type: NodeType = NodeType.COMPONENT
    heightRemFactor: RemFactor
    widthRemFactor: RemFactor
    innerText: Text | None = None
    outerText: Text | None = None
    amg_only: bool = False
    security_class: int | None = None
    technical_capabilities: set[TechnicalCapability] = set()
    classifications: set[EcuClassification] = {EcuClassification.ECU}

    def __hash__(self) -> int:
        return hash(
            (
                self.type,
                self.xRemFactor,
                self.yRemFactor,
                self.heightRemFactor,
                self.widthRemFactor,
                self.innerText,
                self.outerText,
                self.amg_only,
                self.security_class,
                tuple(self.technical_capabilities),
                tuple(self.classifications),
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return hash(self) == hash(other)

    def polygon(self, *, buffer: float = 0.0) -> Polygon:
        """
        Returns the polygon representation of the component's rectangle

        :param buffer: Increase the rectangle's dimensions by `buffer` in all directions
        :type buffer: float
        :return: The polygon representation of the rectangle
        :rtype: Polygon
        """
        _x_rem_factor = self.xRemFactor
        _y_rem_factor = self.yRemFactor
        _width_rem_factor = self.widthRemFactor
        _height_rem_factor = self.heightRemFactor

        return Polygon(
            (
                (_x_rem_factor - buffer, _y_rem_factor - buffer),
                (_x_rem_factor - buffer, _y_rem_factor + _height_rem_factor + buffer),
                (
                    _x_rem_factor + _width_rem_factor + buffer,
                    _y_rem_factor + _height_rem_factor + buffer,
                ),
                (_x_rem_factor + _width_rem_factor + buffer, _y_rem_factor - buffer),
                (_x_rem_factor - buffer, _y_rem_factor - buffer),
            )
        )


class XorNode(Node):
    """Model for the XOR nodes."""

    type: NodeType = NodeType.XOR
    heightRemFactor: RemFactor
    widthRemFactor: RemFactor
    innerText: Text | None = get_default_text("XOR")

    def __hash__(self) -> int:
        return hash(
            (
                self.type,
                self.xRemFactor,
                self.yRemFactor,
                self.heightRemFactor,
                self.widthRemFactor,
                self.innerText,
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return hash(self) == hash(other)


class TextNode(Node):
    """Model for the text nodes."""

    type: NodeType = NodeType.TEXT
    innerText: Text | None = None

    def __hash__(self) -> int:
        return hash(
            (
                self.type,
                self.xRemFactor,
                self.yRemFactor,
                self.innerText,
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return hash(self) == hash(other)


class WaypointNode(Node):
    """Model for the waypoint nodes."""

    type: NodeType = NodeType.WAYPOINT

    def __hash__(self) -> int:
        return hash(
            (
                self.type,
                self.xRemFactor,
                self.yRemFactor,
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return hash(self) == hash(other)


class ProtocolType(Enum):
    """Enum for the supported protocol types."""

    CAN = "CAN"
    CAN_250 = "CAN_250"
    CAN_500 = "CAN_500"
    CAN_800 = "CAN_800"
    CAN_FD = "CAN_FD"
    FLEX_RAY = "FLEX_RAY"
    ETHERNET = "ETHERNET"
    MOST_ELECTRIC = "MOST_ELECTRIC"
    LIN = "LIN"
    UNKNOWN = "UNKNOWN"
    OTHER = "OTHER"


class Network(BaseModel):
    """Model for the networks."""

    model_config = ConfigDict(extra="forbid")

    protocolType: ProtocolType
    masterId: Annotated[UUID, UuidVersion(4)] | None = Field(
        default=None,
        description="The UUID of the bus master if applicable.",
    )
    amg_only: bool = False
    edges: list[Edge]

    def __hash__(self) -> int:
        return hash(
            (
                self.protocolType,
                self.amg_only,
            )
        )


class Edge(BaseModel):
    """Model for the edges/links between ECUS."""

    model_config = ConfigDict(extra="forbid")

    sourceId: Annotated[UUID, UuidVersion(4)]
    targetId: Annotated[UUID, UuidVersion(4)]
    sourceAttachmentPointX: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Origin is in upper left corner of the respective element, \
x increases to the right.",
    )
    sourceAttachmentPointY: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Origin is in upper left corner of the respective element, \
y increases downwards.",
    )
    targetAttachmentPointX: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Origin is in upper left corner of the respective element, \
x increases to the right.",
    )
    targetAttachmentPointY: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Origin is in upper left corner of the respective element, \
y increases downwards.",
    )

    text: Text | None = None

    def __hash__(self) -> int:
        return hash(
            (
                self.sourceAttachmentPointX,
                self.sourceAttachmentPointY,
                self.targetAttachmentPointX,
                self.targetAttachmentPointY,
                self.text,
            )
        )


NodeUnionType = Union[WaypointNode, TextNode, XorNode, ComponentNode]


class Graph(BaseModel):
    """Model for the graphs of a car architecture."""

    model_config = ConfigDict(extra="forbid")

    label: Text
    nodes: dict[Annotated[UUID, UuidVersion(4)], NodeUnionType]
    networks: list[Network]

    @classmethod
    def get_network_tuple(
        cls, network: Network, graph: Graph
    ) -> tuple[Network, Node | None, tuple[Any, ...]]:
        """
        Get a tuple of (network, network_master, tuple[tuple[edge, source, target]])
        """
        nw_edges: set[tuple[Edge, Node, Node]] = set()
        for edge in network.edges:
            edge_source = graph.nodes.get(edge.sourceId)
            if edge_source is None:
                raise ReferenceError(f"Could not find source node {edge.sourceId}")
            edge_target = graph.nodes.get(edge.targetId)
            if edge_target is None:
                raise ReferenceError(f"Could not find target node {edge.targetId}")
            nw_edges.add((edge, edge_source, edge_target))

        nw_master = graph.nodes.get(network.masterId) if network.masterId else None
        return (network, nw_master, tuple(nw_edges))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        if not self.label == other.label:
            return False

        node_occurrences: dict[NodeUnionType, int] = {}

        # count all node_occurrences in self.nodes
        for node in self.nodes.values():
            if node in node_occurrences:
                node_occurrences[node] += 1
            else:
                node_occurrences[node] = 1

        # count all node_occurrences other.nodes
        for other_node in other.nodes.values():
            if other_node in node_occurrences:
                node_occurrences[other_node] -= 1
            else:
                return False

        if any(item != 0 for item in node_occurrences.values()):
            return False

        # count tuples of (network, network_master, list[tuple[edge, source, target]])
        network_occurences: dict[
            tuple[Network, Node | None, tuple[tuple[Edge, Node, Node]]],
            int,
        ] = {}

        for network in self.networks:
            nw_tuple = self.get_network_tuple(network, self)
            if nw_tuple in network_occurences:
                network_occurences[nw_tuple] += 1
            else:
                network_occurences[nw_tuple] = 1

        for network in other.networks:
            nw_tuple = self.get_network_tuple(network, other)
            if nw_tuple in network_occurences:
                network_occurences[nw_tuple] -= 1
            else:
                return False

        if any(item != 0 for item in network_occurences.values()):
            return False

        return True


class GraphCollection(BaseModel):
    """Model for the collection of graphs."""

    model_config = ConfigDict(
        extra="forbid",
        title="Graph Schema",
    )

    graphs: list[Graph]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.graphs == other.graphs
