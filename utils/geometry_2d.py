from .point import *
from typing import Tuple

Ray = Tuple[Point, Point]
Segment = Tuple[Point, Point]
Line = Tuple[Point, Point]

def intersection(l1: Line, l2: Line):
    """
    Check the intersection between two lines. Return None if they are parallel
    """

def intersection(s1: Segment, s2: Segment):
    """
    Check the intersection between two segments. Return None if they are not intersect
    """

def intersection(r1: Ray, r2: Ray):
    """
    Check the intersection between two rays. Return None if they are not intersect
    """