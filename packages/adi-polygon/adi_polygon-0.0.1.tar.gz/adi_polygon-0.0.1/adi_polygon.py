from __future__ import annotations
from typing import NamedTuple
from dataclasses import dataclass


class Polygon(NamedTuple):
    """
    A polygon returned by the Document Intelligence API.
    If used as the annotation for a Pydantic model, it will be parsed from the
    input JSON array.
    """

    x1: float
    y1: float
    x2: float
    y2: float
    x3: float
    y3: float
    x4: float
    y4: float

    def as_vertices(self) -> Vertices:
        return Vertices(
            Point(self.x1, self.y1),
            Point(self.x2, self.y2),
            Point(self.x3, self.y3),
            Point(self.x4, self.y4),
        )


class Point(NamedTuple):
    x: float
    y: float

    def as_mutable(self) -> PointMutable:
        return PointMutable(self.x, self.y)


class Vertices(NamedTuple):
    """
    An alternative representation of the data found in a Polygon tuple returned
    by the Document Intelligence API.
    """

    top_left: Point
    top_right: Point
    bottom_right: Point
    bottom_left: Point

    def as_polygon(self) -> Polygon:
        return Polygon(
            x1=self.top_left.x,
            y1=self.top_left.y,
            x2=self.top_right.x,
            y2=self.top_right.y,
            x3=self.bottom_right.x,
            y3=self.bottom_right.y,
            x4=self.bottom_left.x,
            y4=self.bottom_left.y,
        )

    def as_mutable(self) -> VerticesMutable:
        return VerticesMutable(
            self.top_left.as_mutable(),
            self.top_right.as_mutable(),
            self.bottom_right.as_mutable(),
            self.bottom_left.as_mutable(),
        )


@dataclass
class PointMutable:
    x: float
    y: float

    def as_tuple(self) -> Point:
        return Point(self.x, self.y)


@dataclass
class VerticesMutable:
    top_left: PointMutable
    top_right: PointMutable
    bottom_right: PointMutable
    bottom_left: PointMutable

    def as_tuple(self) -> Vertices:
        return Vertices(
            self.top_left.as_tuple(),
            self.top_right.as_tuple(),
            self.bottom_right.as_tuple(),
            self.bottom_left.as_tuple(),
        )
