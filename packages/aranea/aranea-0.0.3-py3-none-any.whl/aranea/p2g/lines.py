"""
Module to extract network lines from the PDF document.
"""

import logging
import uuid
from dataclasses import dataclass
from itertools import combinations, count
from typing import Annotated, Any
from uuid import UUID, uuid4

from pymupdf.pymupdf import Page
from shapely import LineString, Point

from aranea.models.graph_model import (ComponentNode, Edge, Network, NodeType,
                                       NodeUnionType, ProtocolType,
                                       WaypointNode, XorNode)
from aranea.p2g.util import REM, gendocstring

Color = tuple[int, int, int]

logger = logging.getLogger(__name__)


@dataclass
class LineSegment:
    """
    Internal class for temporarily storing network line segments
    """

    p1: Point
    p2: Point
    color: Color
    width: float
    bus_id: int | None = None
    source_id: UUID | None = None
    target_id: UUID | None = None
    source_attachment_point_x: float | None = None
    source_attachment_point_y: float | None = None
    target_attachment_point_x: float | None = None
    target_attachment_point_y: float | None = None


@gendocstring
def __are_lines_connected(
    line1: Annotated[LineSegment, "first line"],
    line2: Annotated[LineSegment, "second line"],
    merge_tolerance: Annotated[
        float, "the tolerance of the distance between the two lines to be merged"
    ],
    parallel_tolerance: Annotated[
        float, "the tolerance of the parallel distance between the two lines to be merged"
    ],
    alignment_offset: Annotated[float, "the offset at which a line is still considered parallel"],
) -> Annotated[bool, "A Boolean"]:
    """
    checks whether two lines are connected.
    """

    # line1 is horizontal
    if (
        abs(line1.p1.y - line1.p2.y) <= alignment_offset
        and abs(line2.p1.y - line2.p2.y) <= alignment_offset
    ):
        if abs(line1.p1.y - line2.p1.y) <= parallel_tolerance:
            if (
                max(line1.p1.x, line1.p2.x) >= min(line2.p1.x, line2.p2.x) - merge_tolerance
                and max(line2.p1.x, line2.p2.x) >= min(line1.p1.x, line1.p2.x) - merge_tolerance
            ):
                return True

    # line1 is vertical
    elif (
        abs(line1.p1.x - line1.p2.x) <= alignment_offset
        and abs(line2.p1.x - line2.p2.x) <= alignment_offset
    ):
        if abs(line1.p1.x - line2.p1.x) <= parallel_tolerance:
            if (
                max(line1.p1.y, line1.p2.y) >= min(line2.p1.y, line2.p2.y) - merge_tolerance
                and max(line2.p1.y, line2.p2.y) >= min(line1.p1.y, line1.p2.y) - merge_tolerance
            ):
                return True

    return False


@gendocstring
def __combine_lines(
    lines: Annotated[list[LineSegment], "A list of line dictionaries"],
    merge_tolerance: Annotated[
        float, "Maximum distance allowed between endpoints to consider lines connected"
    ],
    parallel_tolerance: Annotated[
        float, "Maximum angle deviation allowed to consider lines parallel"
    ],
    alignment_offset: Annotated[float, "Offset for adjusting alignment when merging lines"],
) -> Annotated[list[LineSegment], "A list of combined lines"]:
    """
    Merges connected lines with the same bus ID and which fulfill the tolerance values into a
    single line.
    """
    i = 0
    while i < len(lines):
        line1 = lines[i]
        combined = False
        for j in range(i + 1, len(lines)):
            line2 = lines[j]

            if line1.bus_id == line2.bus_id and __are_lines_connected(
                line1, line2, merge_tolerance, parallel_tolerance, alignment_offset
            ):

                if abs(line1.p1.y - line1.p2.y) <= abs(line1.p1.x - line1.p2.x):  # horizontal
                    new_x1 = min(line1.p1.x, line1.p2.x, line2.p1.x, line2.p2.x)
                    new_y1 = line1.p1.y
                    new_x2 = max(line1.p1.x, line1.p2.x, line2.p1.x, line2.p2.x)
                    new_y2 = line1.p1.y
                else:  # vertical
                    new_x1 = line1.p1.x
                    new_y1 = min(line1.p1.y, line1.p2.y, line2.p1.y, line2.p2.y)
                    new_x2 = line1.p1.x
                    new_y2 = max(line1.p1.y, line1.p2.y, line2.p1.y, line2.p2.y)

                # new line
                new_line = LineSegment(
                    p1=Point(new_x1, new_y1),
                    p2=Point(new_x2, new_y2),
                    color=line1.color,
                    width=line1.width,
                    bus_id=line1.bus_id,
                    source_id=line1.source_id,
                    target_id=line1.target_id,
                    source_attachment_point_x=line1.source_attachment_point_x,
                    source_attachment_point_y=line1.source_attachment_point_y,
                    target_attachment_point_x=line1.target_attachment_point_x,
                    target_attachment_point_y=line1.target_attachment_point_y,
                )

                # delete old line
                lines.pop(j)
                lines.pop(i)

                lines.append(new_line)
                combined = True
                break

        if not combined:
            i += 1

    return lines


@gendocstring
def __assign_bus_ids_to_lines(
    lines: Annotated[list[LineSegment], "A list of line segments"],
    busid_tolerance: Annotated[float, "Tolerance value used to determine if lines are connected"],
) -> None:
    """
    Groups lines by their touch and color, then assigns unique bus IDs.
    """
    next_bus_id = count(1)  # Generator for Bus-IDs
    color_groups: dict[Color, list[LineSegment]] = {}

    for line in lines:
        color = line.color
        if color not in color_groups:
            color_groups[color] = []
        color_groups[color].append(line)

    for color, color_lines in color_groups.items():
        visited: set[int] = set()

        for line in color_lines:
            if line.bus_id is not None:
                continue

            current_bus_id = next(next_bus_id)
            __assign_bus_id_to_connected_lines(
                line, color_lines, visited, current_bus_id, busid_tolerance
            )


@gendocstring
def __assign_bus_id_to_connected_lines(
    line: Annotated[LineSegment, "Current line"],
    color_lines: Annotated[list[LineSegment], "Lines of the same color"],
    visited: Annotated[set[int], "Set of visited lines"],
    bus_id: Annotated[int, "ID of the current bus system"],
    tolerance: float,
) -> None:
    """
    Function to assign bus IDs to connected lines.
    """
    queue = [line]
    while queue:
        current_line = queue.pop()
        if id(current_line) in visited:
            continue
        visited.add(id(current_line))
        current_line.bus_id = bus_id

        # find connected lines and append them to the queue
        for other_line in color_lines:
            if id(other_line) not in visited and __lines_touch(current_line, other_line, tolerance):
                queue.append(other_line)


@gendocstring
def __lines_touch(
    line1: Annotated[LineSegment, "First line"],
    line2: Annotated[LineSegment, "Second line"],
    tolerance: Annotated[float, "Tolerance for the overlap"],
) -> Annotated[bool, "True if the lines overlap, otherwise False"]:
    """
    Checks whether two lines overlap in the area.
    """
    line1_string = LineString([line1.p1, line1.p2]).buffer(tolerance)
    line2_string = LineString([line2.p1, line2.p2]).buffer(tolerance)

    return line1_string.intersects(line2_string)  # type: ignore


@gendocstring
def __extend_line_to_intersect(
    line: Annotated[LineSegment, "The current line"],
    lines: Annotated[list[LineSegment], "List of all lines"],
    tolerance: Annotated[float, "Tolerance for equal coordinates"],
) -> Annotated[LineSegment, "The extended line"]:
    """
    Extends a line so that it ends exactly at intersections with other lines of the same bus ID.
    """
    for other_line in lines:
        if other_line == line or other_line.bus_id != line.bus_id:
            continue

        ox1, oy1, ox2, oy2 = (
            other_line.p1.x,
            other_line.p1.y,
            other_line.p2.x,
            other_line.p2.y,
        )

        # Line is horizontal
        if abs(line.p1.y - line.p2.y) <= tolerance:
            if (
                any(abs(ox - line.p1.x) <= tolerance for ox in (ox1, ox2))
                or any(abs(ox - line.p2.x) <= tolerance for ox in (ox1, ox2))
            ) and (
                oy1 <= line.p1.y <= oy2
                or oy1 <= line.p2.y <= oy2
                or line.p1.y <= oy1 <= line.p2.y
                or line.p1.y <= oy2 <= line.p2.y
            ):
                return LineSegment(
                    p1=Point(min(line.p1.x, line.p2.x, ox1, ox2), line.p1.y),
                    p2=Point(max(line.p1.x, line.p2.x, ox1, ox2), line.p1.y),
                    color=line.color,
                    width=line.width,
                    bus_id=line.bus_id,
                    source_id=line.source_id,
                    target_id=line.target_id,
                    source_attachment_point_x=line.source_attachment_point_x,
                    source_attachment_point_y=line.source_attachment_point_y,
                    target_attachment_point_x=line.target_attachment_point_x,
                    target_attachment_point_y=line.target_attachment_point_y,
                )

        # Line is vertical
        elif abs(line.p1.x - line.p2.x) <= tolerance:
            if (
                any(abs(oy - line.p1.y) <= tolerance for oy in (oy1, oy2))
                or any(abs(oy - line.p2.y) <= tolerance for oy in (oy1, oy2))
            ) and (
                ox1 <= line.p1.x <= ox2
                or ox1 <= line.p2.x <= ox2
                or line.p1.x <= ox1 <= line.p2.x
                or line.p1.x <= ox2 <= line.p2.x
            ):
                return LineSegment(
                    p1=Point(line.p1.x, min(line.p1.y, line.p2.y, oy1, oy2)),
                    p2=Point(line.p1.x, max(line.p1.y, line.p2.y, oy1, oy2)),
                    color=line.color,
                    width=line.width,
                    bus_id=line.bus_id,
                    source_id=line.source_id,
                    target_id=line.target_id,
                    source_attachment_point_x=line.source_attachment_point_x,
                    source_attachment_point_y=line.source_attachment_point_y,
                    target_attachment_point_x=line.target_attachment_point_x,
                    target_attachment_point_y=line.target_attachment_point_y,
                )

    return line


@gendocstring
def __cut_line_under_nodes(
    line: Annotated[LineSegment, "The line segment"],
    nodes: Annotated[
        dict[uuid.UUID, XorNode | ComponentNode], "A dictionary of nodes with their geometry data"
    ],
    rem: REM,
) -> Annotated[LineSegment, "The adjusted line or None if it has been completely removed"]:
    """
    Cuts a line so that it no longer lies under the specified nodes.
    """

    source_attachment_point_x: float | None = None
    source_attachment_point_y: float | None = None
    target_attachment_point_x: float | None = None
    target_attachment_point_y: float | None = None
    source_id: uuid.UUID | None = None
    target_id: uuid.UUID | None = None
    for node_uuid, node in nodes.items():
        # Check whether a point on the line lies within the node
        if (
            node.xRemFactor * rem <= line.p1.x <= node.xRemFactor * rem + node.widthRemFactor * rem
            and node.yRemFactor * rem
            <= line.p1.y
            <= node.yRemFactor * rem + node.heightRemFactor * rem
        ):
            intersection = __line_intersects_rect(line, node, rem)
            if intersection is not None:
                source_attachment_point_x, source_attachment_point_y = intersection
                source_id = node_uuid

        if (
            node.xRemFactor * rem <= line.p2.x <= node.xRemFactor * rem + node.widthRemFactor * rem
            and node.yRemFactor * rem
            <= line.p2.y
            <= node.yRemFactor * rem + node.heightRemFactor * rem
        ):
            intersection = __line_intersects_rect(line, node, rem)
            if intersection is not None:
                target_attachment_point_x, target_attachment_point_y = intersection
                target_id = node_uuid

    return LineSegment(
        p1=line.p1,
        p2=line.p2,
        color=line.color,
        width=line.width,
        bus_id=line.bus_id,
        source_id=source_id,
        target_id=target_id,
        source_attachment_point_x=source_attachment_point_x,
        source_attachment_point_y=source_attachment_point_y,
        target_attachment_point_x=target_attachment_point_x,
        target_attachment_point_y=target_attachment_point_y,
    )


@gendocstring
def __line_intersects_rect(
    line: Annotated[LineSegment, "The line segment"],
    node: Annotated[XorNode | ComponentNode, "The rectangle represented as a `Node`"],
    rem: REM,
) -> Annotated[
    tuple[float, float] | None,
    "The intersection point as a tuple (x, y), relative from the origin of the"
    "rectangle, only if the line intersects any edge of the rectangle, otherwise"
    "`None`",
]:
    """
    Determines if a line segment intersects a rectangle and returns the intersection point.
    """
    x_min = node.xRemFactor * rem
    y_min = node.yRemFactor * rem
    x_max = (node.xRemFactor + node.widthRemFactor) * rem
    y_max = (node.yRemFactor + node.heightRemFactor) * rem

    # edges of rectangle
    edges = [
        (Point(x_min, y_min), Point(x_max, y_min)),  # upper edge
        (Point(x_min, y_max), Point(x_max, y_max)),  # lower edge
        (Point(x_min, y_min), Point(x_min, y_max)),  # left edge
        (Point(x_max, y_min), Point(x_max, y_max)),  # right edge
    ]

    for edge_start, edge_end in edges:
        intersection: Point | None = __line_intersection(line, edge_start, edge_end)

        if intersection:
            relative_x: float = (intersection.x - x_min) / (x_max - x_min)
            relative_y: float = (intersection.y - y_min) / (y_max - y_min)
            return relative_x, relative_y
    return None  # no intersection found


@gendocstring
def __line_intersection(
    line: Annotated[LineSegment, "The first line segment"],
    p3: Annotated[Point, "The first point of the second line"],
    p4: Annotated[Point, "The second point of the second line"],
) -> Annotated[
    Point | None,
    "The intersection point as a tuple (x, y) if the"
    "lines intersect within the segment boundaries, otherwise `None`",
]:
    """
    Calculates the intersection of a line segment with another line that is defined by two
    points.
    """

    denominator = (line.p1.x - line.p2.x) * (p3.y - p4.y) - (line.p1.y - line.p2.y) * (p3.x - p4.x)
    if denominator == 0:
        return None  # parallel

    t = ((line.p1.x - p3.x) * (p3.y - p4.y) - (line.p1.y - p3.y) * (p3.x - p4.x)) / denominator
    u = (
        (line.p1.x - p3.x) * (line.p1.y - line.p2.y) - (line.p1.y - p3.y) * (line.p1.x - line.p2.x)
    ) / denominator

    if 0 <= t <= 1 and 0 <= u <= 1:
        x = line.p1.x + t * (line.p2.x - line.p1.x)
        y = line.p1.y + t * (line.p2.y - line.p1.y)
        return Point(x, y)
    return None


@gendocstring
def __find_existing_waypoint(
    point: Annotated[Point, "The point"],
    waypoints: Annotated[dict[uuid.UUID, WaypointNode], "The waypoints"],
    rem: REM,
) -> Annotated[uuid.UUID | None, "The waypoint's UUID or None"]:
    """
    Finds an existing waypoint by coordinates.
    """
    for waypoint_id, waypoint in waypoints.items():
        if waypoint.xRemFactor * rem == point.x and waypoint.yRemFactor * rem == point.y:
            return waypoint_id
    return None


@gendocstring
def __get_waypoints(
    lines: Annotated[list[LineSegment], "List of lines"],
    rem: REM,
) -> Annotated[
    tuple[dict[uuid.UUID, WaypointNode], list[LineSegment]], "A tuple of Waypoints and LineSegments"
]:
    """
    Assigns waypoints to line segments by generating `source_id` and `target_id` where missing.
    """
    waypoints: dict[uuid.UUID, WaypointNode] = {}

    for line in lines:
        # Check for existing source waypoint
        if line.source_id is None:
            source_id = __find_existing_waypoint(line.p1, waypoints, rem)
            if source_id is None:  # Create new waypoint if not found
                source_id = uuid4()
                waypoints[source_id] = WaypointNode(
                    type=NodeType.WAYPOINT,
                    xRemFactor=line.p1.x / rem,
                    yRemFactor=line.p1.y / rem,
                )
            line.source_id = source_id

        # Check for existing target waypoint
        if line.target_id is None:
            target_id = __find_existing_waypoint(line.p2, waypoints, rem)
            if target_id is None:  # Create new waypoint if not found
                target_id = uuid4()
                waypoints[target_id] = WaypointNode(
                    type=NodeType.WAYPOINT,
                    xRemFactor=line.p2.x / rem,
                    yRemFactor=line.p2.y / rem,
                )
            line.target_id = target_id

    return waypoints, lines


@gendocstring
def __split_line_at_waypoint(
    lines: Annotated[list[LineSegment], "List of line segments to process"],
    waypoints: Annotated[
        dict[uuid.UUID, WaypointNode], "Dictionary of waypoints to check, indexed by UUID"
    ],
    tolerance: Annotated[float, "Tolerance for determining if a waypoint lies on a line"],
    rem: REM,
) -> Annotated[list[LineSegment], "Updated list of line segments with lines split at waypoints"]:
    """
    Splits lines into segments at specified waypoints if they lie on the line within a given
    tolerance.
    """
    lines_to_append: list[LineSegment] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        waypoints_on_line: list[tuple[Point, uuid.UUID | None, float | None, float | None]] = []

        for waypoint_uuid, waypoint in waypoints.items():

            # Skip if waypoint is at the start or end of the line
            if (
                waypoint.xRemFactor * rem != line.p1.x or waypoint.yRemFactor * rem != line.p1.y
            ) and (
                waypoint.xRemFactor * rem != line.p2.x or waypoint.yRemFactor * rem != line.p2.y
            ):
                # Check if the waypoint is on the straight line
                cross_product = (waypoint.xRemFactor * rem - line.p1.x) * (
                    line.p2.y - line.p1.y
                ) - (waypoint.yRemFactor * rem - line.p1.y) * (line.p2.x - line.p1.x)
                if abs(cross_product) <= tolerance:
                    # Check if the waypoint is within the segment boundaries
                    if (
                        min(line.p1.x, line.p2.x) - tolerance
                        <= waypoint.xRemFactor * rem
                        <= max(line.p1.x, line.p2.x) + tolerance
                        and min(line.p1.y, line.p2.y) - tolerance
                        <= waypoint.yRemFactor * rem
                        <= max(line.p1.y, line.p2.y) + tolerance
                    ):
                        waypoints_on_line.append(
                            (
                                Point(waypoint.xRemFactor * rem, waypoint.yRemFactor * rem),
                                waypoint_uuid,
                                None,
                                None,
                            )
                        )

        if waypoints_on_line:
            if line.source_id is None:
                raise ValueError("sourceId must be a UUID")
            if line.target_id is None:
                raise ValueError("targetId must be a UUID")

            # Include start and end points of the line
            waypoints_on_line.append(
                (
                    line.p1,
                    line.source_id,
                    line.source_attachment_point_x,
                    line.source_attachment_point_y,
                )
            )
            waypoints_on_line.append(
                (
                    line.p2,
                    line.target_id,
                    line.target_attachment_point_x,
                    line.target_attachment_point_y,
                )
            )

            # Sort waypoints to split the line correctly
            sorted_waypoints = sorted(waypoints_on_line, key=lambda p: (p[0].x, p[0].y))

            # Generate new line segments
            for j in range(len(sorted_waypoints) - 1):
                lines_to_append.append(
                    LineSegment(
                        p1=sorted_waypoints[j][0],
                        p2=sorted_waypoints[j + 1][0],
                        color=line.color,
                        width=line.width,
                        bus_id=line.bus_id,
                        source_id=sorted_waypoints[j][1],
                        target_id=sorted_waypoints[j + 1][1],
                        source_attachment_point_x=sorted_waypoints[j][2],
                        source_attachment_point_y=sorted_waypoints[j][3],
                        target_attachment_point_x=sorted_waypoints[j + 1][2],
                        target_attachment_point_y=sorted_waypoints[j + 1][3],
                    )
                )

            # Remove the original line
            lines.pop(i)
        else:
            # Only increment if the line was not removed
            i += 1

    # Add new lines to the list
    lines.extend(lines_to_append)

    return lines


def __remove_non_diagram_lines(
    nodes: dict[uuid.UUID, NodeUnionType],
    networks: list[Network],
    waypoints: dict[uuid.UUID, WaypointNode],
) -> tuple[list[Network], dict[uuid.UUID, WaypointNode]]:
    """
    Removes networks which only connect waypoints and filters out those waypoints.

    :param nodes: A dictionary of nodes with their geometry data.
    :type nodes: dict[uuid.UUID, Any]
    :param networks: A list of Network objects.
    :type networks: list[Network]
    :return: A filtered list of Network objects.
    :rtype: list[Network]
    """
    waypoint_id_list: list[uuid.UUID] = []

    def has_ecu_classification(node_id: uuid.UUID) -> bool:
        node = nodes.get(node_id)
        if node is not None and node.type != NodeType.WAYPOINT:
            return True
        waypoint_id_list.append(node_id)
        return False

    filtered_networks: list[Network] = []
    for network in networks:
        if any(
            has_ecu_classification(edge.sourceId) or has_ecu_classification(edge.targetId)
            for edge in network.edges
        ):
            filtered_networks.append(network)
        else:
            for edge in network.edges:
                if edge.sourceId in waypoints:
                    waypoints.pop(edge.sourceId)
                if edge.targetId in waypoints:
                    waypoints.pop(edge.targetId)

    return filtered_networks, waypoints


@gendocstring
def get_lines(
    page: Page,
    nodes: Annotated[dict[uuid.UUID, Any], "A dictionary of nodes with their geometry data"],
    rem: REM,
    *,
    lines_min_width: Annotated[float, "The minimum width of a line or curve to be considered"] = 1,
    lines_distance_tolerance: Annotated[
        float, "The distance two lines can have to still be considered as the same network"
    ] = 2,
    lines_merge_tolerance: Annotated[
        float, "The tolerance of the distance between the two lines to be merged"
    ] = 2,
    lines_parallel_tolerance: Annotated[
        float, "The tolerance of the parallel distance between the two lines to be merged"
    ] = 1,
    lines_alignment_offset: Annotated[
        float, "The offset at which a line is still considered parallel"
    ] = 1,
    lines_busid_tolerance: Annotated[
        float, "The distance on which two lines still be considered as the same network"
    ] = 0.8,
    lines_extension_tolerance: Annotated[
        float, "The tolerance to which a line is still extended to meet another line"
    ] = 2,
    lines_split_tolerance: Annotated[
        float, "Tolerance for determining if a waypoint lies on a line"
    ] = 0.05,
    **_: Any,  # ignore any additional keyword arguments
) -> Annotated[
    tuple[list[Network], dict[uuid.UUID, WaypointNode]],
    "A list of `Network` objects and a dictionary of type `WaypointNode`",
]:
    """
    Extracts lines and curves from the current page, processes them and generates `WaypointNode` s
    """

    drawings = page.get_drawings()
    lines: list[LineSegment] = []
    curves: list[LineSegment] = []

    # Collect lines and curves
    for drawing in drawings:
        # Ignore non stroke-only paths
        if drawing["type"] != "s":
            continue
        for item in drawing["items"]:
            if item[0] not in ["l", "c"]:
                continue

            c = drawing["color"]
            color = (0, 0, 0)
            if not c or len(c) != 3:
                logger.warning("Invalid color format: %s", c)
            else:
                color = (c[0] * 255, c[1] * 255, c[2] * 255)
            width = drawing["width"]
            if width > lines_min_width:
                if item[0] == "l":
                    lines.append(
                        LineSegment(p1=Point(item[1]), p2=Point(item[2]), color=color, width=width)
                    )
                elif item[0] == "c":
                    curves.append(
                        LineSegment(p1=Point(item[1]), p2=Point(item[-1]), color=color, width=width)
                    )
    # Assign bus IDs for touching lines of the same color
    __assign_bus_ids_to_lines(lines, lines_busid_tolerance)

    # Merging adjacent curves of the same color
    connected_curves: list[LineSegment] = []
    while curves:
        current_curve = curves.pop(0)

        # Repeated connection until there are no more connections
        while True:
            for other_curve in curves.copy():
                if current_curve.color == other_curve.color and __lines_touch(
                    current_curve, other_curve, lines_distance_tolerance
                ):
                    points: list[Point] = [
                        current_curve.p1,
                        current_curve.p2,
                        other_curve.p1,
                        other_curve.p2,
                    ]

                    # Find the two furthest points and set them as `start` and `end`.
                    max_start, max_end = max(
                        combinations(points, 2), key=lambda _p: _p[0].distance(_p[1])
                    )
                    current_curve.p1 = max_start
                    current_curve.p2 = max_end
                    curves.remove(other_curve)
                    break  # Start over to look for more connections
            else:
                break  # Exit the while loop if no connection was found

        # Find nearby lines and assign 'bus_id'
        for line in lines:
            l = LineString([line.p1, line.p2])
            if current_curve.p1.buffer(lines_distance_tolerance).intersects(
                l
            ) or current_curve.p2.buffer(lines_distance_tolerance).intersects(l):
                if not current_curve.bus_id:
                    current_curve.bus_id = line.bus_id
                else:
                    changing_bus_id = line.bus_id
                    for l in lines:
                        if l.bus_id == changing_bus_id:
                            l.bus_id = current_curve.bus_id

        # Add the connected curve to the list of lines
        connected_curves.append(current_curve)

    for curve in connected_curves:
        for line in lines:
            if curve.bus_id == line.bus_id:
                break  # Curve hat eine gültige bus_id
        else:
            # Kein gültiges bus_id gefunden, prüfen auf Nähe zu einer Linie
            for line in lines:
                l = LineString([line.p1, line.p2])
                if curve.p1.buffer(lines_distance_tolerance).intersects(l) or curve.p2.buffer(
                    lines_distance_tolerance
                ).intersects(l):
                    curve.bus_id = line.bus_id
                    break

    # Save connected curves as lines
    lines.extend(connected_curves)
    while True:
        new_lines = __combine_lines(
            lines, lines_merge_tolerance, lines_parallel_tolerance, lines_alignment_offset
        )
        if len(new_lines) == len(lines):
            break
        lines = new_lines
    lines = [__extend_line_to_intersect(line, lines, lines_extension_tolerance) for line in lines]
    lines = [__cut_line_under_nodes(line, nodes, rem) for line in lines]
    waypoints, lines = __get_waypoints(lines, rem)
    lines = __split_line_at_waypoint(lines, waypoints, lines_split_tolerance, rem)

    bus_id_groups: dict[int | None, list[LineSegment]] = {}
    for line in lines:
        bus_id = line.bus_id
        if bus_id not in bus_id_groups:
            bus_id_groups[bus_id] = []
        bus_id_groups[bus_id].append(line)

    networks: list[Network] = []

    for bus_id_group in bus_id_groups.values():
        edges: list[Edge] = []
        for line in bus_id_group:
            if line.source_id is None or line.target_id is None:
                raise ValueError(f"Source ID or target ID of line {line} is empty")
            edge = Edge(
                sourceId=line.source_id,
                targetId=line.target_id,
                sourceAttachmentPointX=line.source_attachment_point_x,
                sourceAttachmentPointY=line.source_attachment_point_y,
                targetAttachmentPointX=line.target_attachment_point_x,
                targetAttachmentPointY=line.target_attachment_point_y,
            )
            edges.append(edge)
        network = Network(
            protocolType=ProtocolType.UNKNOWN,
            amg_only=False,
            edges=edges,
        )
        networks.append(network)

    networks, waypoints = __remove_non_diagram_lines(nodes, networks, waypoints)

    return networks, waypoints
