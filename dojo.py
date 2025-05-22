import math
import re
from typing import List, Tuple, Union, Optional




class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other: "Point") -> float:
        """Calculate Euclidean distance between two points"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)




def intersect_segments(p1: Point, p2: Point, p3: Point, p4: Point) -> Optional[Point]:
    """Calculate the exact intersection point of two line segments (p1,p2) and (p3,p4).
    Returns the intersection point or None if they do not intersect or are collinear.
    """
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y
    x4, y4 = p4.x, p4.y

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if den == 0:
        return None

    t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    u_num = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))

    t = t_num / den
    u = u_num / den

    if 0 <= t <= 1 and 0 <= u <= 1:
        intersect_x = x1 + t * (x2 - x1)
        intersect_y = y1 + t * (y2 - y1)
        return Point(intersect_x, intersect_y)

    return None

def assert_points_equal(p_actual: Optional[Point], p_expected: Optional[Point], test_name: str, tolerance=1e-9):
    if p_actual is None and p_expected is None:
        return # Test passed silently
    if p_actual is None or p_expected is None:
        assert False, f"{test_name} Failed: Expected {p_expected}, Got {p_actual}"
    
    assert p_actual is not None and p_expected is not None # for type checker
    assert math.isclose(p_actual.x, p_expected.x, abs_tol=tolerance) and \
           math.isclose(p_actual.y, p_expected.y, abs_tol=tolerance), \
           f"{test_name} Failed: Expected Point({p_expected.x},{p_expected.y}), Got Point({p_actual.x},{p_actual.y})"
    # Test passed silently


def test_intersect_segments():
    print("\nRunning tests for intersect_segments...")

    # Test 1: Standard Intersection
    p1, p2 = Point(0, 0), Point(4, 4)
    p3, p4 = Point(0, 4), Point(4, 0)
    expected = Point(2, 2)
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 1 (Standard Intersection)")

    # Test 2: No Intersection - Parallel
    p1, p2 = Point(0, 0), Point(2, 2)
    p3, p4 = Point(0, 1), Point(2, 3) # y = x+1
    expected = None
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 2 (No Intersection - Parallel)")

    # Test 3: No Intersection - Collinear, No Overlap
    p1, p2 = Point(0, 0), Point(1, 0)
    p3, p4 = Point(2, 0), Point(3, 0)
    expected = None # den = 0
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 3 (No Intersection - Collinear, No Overlap)")

    # Test 4: No Intersection - Lines Intersect Outside Segment Boundaries
    p1, p2 = Point(0, 0), Point(2, 0) # Segment on x-axis
    p3, p4 = Point(1, 1), Point(1, 2) # Vertical segment x=1, above x-axis
    # Lines intersect at (1,0), but this is outside p3-p4 (u < 0)
    expected = None
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 4 (No Intersection - Outside Segment Boundaries)")

    # Test 5: Intersection at an Endpoint (Shared Endpoint)
    p1, p2 = Point(0, 0), Point(2, 2)
    p3, p4 = Point(2, 2), Point(3, 0)
    expected = Point(2, 2)
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 5 (Intersection at Shared Endpoint)")

    # Test 6: Intersection at an Endpoint (Mid-segment for other)
    p1, p2 = Point(0, 0), Point(2, 0)
    p3, p4 = Point(1, -1), Point(1, 1)
    expected = Point(1, 0)
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 6 (Intersection at Endpoint, Mid-segment for other)")

    # Test 7: Collinear - Overlapping Segments (Still expect None due to den=0)
    p1, p2 = Point(0, 0), Point(2, 0)
    p3, p4 = Point(1, 0), Point(3, 0)
    expected = None # den = 0
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 7 (Collinear - Overlapping)")

    # Test 8: Collinear - One Segment Contains Another (Still expect None due to den=0)
    p1, p2 = Point(0, 0), Point(3, 0)
    p3, p4 = Point(1, 0), Point(2, 0)
    expected = None # den = 0
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 8 (Collinear - Contained)")

    # Test 9: Horizontal and Vertical Intersection
    p1, p2 = Point(0, 1), Point(4, 1)
    p3, p4 = Point(2, 0), Point(2, 3)
    expected = Point(2, 1)
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 9 (Horizontal/Vertical Intersection)")

    # Test 10: "T" Intersection (Endpoint of one on the other segment)
    p1, p2 = Point(0, 2), Point(4, 2)
    p3, p4 = Point(2, 0), Point(2, 2) # p4 is on p1p2
    expected = Point(2, 2)
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 10 (T Intersection)")

    # Test 11: Floating Point Values
    p1, p2 = Point(0.5, 0.5), Point(2.5, 2.5)
    p3, p4 = Point(0.5, 2.5), Point(2.5, 0.5)
    expected = Point(1.5, 1.5)
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 11 (Floating Point Values)")

    # Test 12: Segments just touch (Vertex touching an edge)
    p1, p2 = Point(0, 0), Point(2, 0) # Horizontal segment
    p3, p4 = Point(1, 0), Point(1, 2) # Vertical, starts on horizontal
    expected = Point(1, 0)
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 12 (Vertex Touching Edge)")

    # Test 13: Segments meet at a common vertex, but don't cross (V shape)
    p1, p2 = Point(0, 0), Point(1, 1)
    p3, p4 = Point(1, 1), Point(2, 0)
    expected = Point(1, 1)
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 13 (Meet at Common Vertex)")

    # Test 14: Segments are far apart and not parallel
    p1, p2 = Point(0, 0), Point(1, 1)
    p3, p4 = Point(5, 5), Point(6, 4)
    expected = None
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 14 (Far Apart, Not Parallel)")

    # Test 15: One segment is a point (p1=p2) - on the other segment
    p1, p2 = Point(1, 1), Point(1, 1)
    p3, p4 = Point(0, 0), Point(2, 2)
    expected = None # den = 0
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 15 (One Segment is Point - On Other)")
    
    # Test 16: One segment is a point (p1=p2) - not on the other segment
    p1, p2 = Point(5,5), Point(5,5)
    p3, p4 = Point(0,0), Point(2,2)
    expected = None # den = 0
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 16 (One Segment is Point - Not On Other)")

    # Test 17: General case - no intersection - lines are not parallel
    p1, p2 = Point(0,0), Point(1,0) # seg on x-axis
    p3, p4 = Point(0,1), Point(1,1) # seg on y=1
    expected = None # Parallel, den=0 if slope diff used for den, let's check current den
    # den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    # p1(0,0) p2(1,0) -> x1-x2=-1, y1-y2=0
    # p3(0,1) p4(1,1) -> x3-x4=-1, y3-y4=0
    # den = (-1)*(0) - (0)*(-1) = 0. So, parallel.
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 17 (Parallel Horizontal Lines)")
    
    # Test 18: Another general case - no intersection
    p1, p2 = Point(0,0), Point(0,1) # seg on y-axis
    p3, p4 = Point(1,0), Point(1,1) # seg on x=1
    # den = (0-0)*(0-1) - (0-1)*(1-1) = 0 - (-1)*0 = 0. Parallel.
    result = intersect_segments(p1, p2, p3, p4)
    assert_points_equal(result, expected, "Test 18 (Parallel Vertical Lines)")

    print("\nAll intersect_segments tests completed.")

class Polygon:
    def __init__(self, points: List[Point]):
        """Initialize a polygon with a list of points"""
        if len(points) < 3:
            raise ValueError("A polygon must have at least 3 points")

        # Ensure the polygon is closed (first point equals last point)
        if points[0].x != points[-1].x or points[0].y != points[-1].y:
            points.append(Point(points[0].x, points[0].y))

        self.points = points

    def __repr__(self) -> str:
        return f"Polygon({len(self.points)} points)"

    def area(self) -> float:
        """Calculate the area of the polygon using the Shoelace formula"""
        return abs(self.signed_area())

    def signed_area(self) -> float:
        n = (
            len(self.points) - 1
        )  # Subtract 1 because the last point is the same as the first
        area = 0.0

        for i in range(n):
            area += (
                self.points[i].x * self.points[i + 1].y
                - self.points[i + 1].x * self.points[i].y
            )

        return area / 2.0

    def center_of_mass(self) -> Point:
        """Calculate the center of mass (centroid) of the polygon"""
        n = (
            len(self.points) - 1
        )  # Subtract 1 because the last point is the same as the first
        cx, cy = 0.0, 0.0
        signed_area = (
            self.signed_area() * 6.0
        )  # Area multiplied by 6 for the centroid formula

        for i in range(n):
            factor = (
                self.points[i].x * self.points[i + 1].y
                - self.points[i + 1].x * self.points[i].y
            )
            cx += (self.points[i].x + self.points[i + 1].x) * factor
            cy += (self.points[i].y + self.points[i + 1].y) * factor

        return Point(cx / signed_area, cy / signed_area)

    def contains_point(self, point: Point) -> bool:
        """Check if a point is inside the polygon using ray casting algorithm"""
        n = len(self.points) - 1
        inside = False

        p1x, p1y = self.points[0].x, self.points[0].y
        for i in range(n + 1):
            p2x, p2y = self.points[i % n].x, self.points[i % n].y

            if (
                point.y > min(p1y, p2y)
                and point.y <= max(p1y, p2y)
                and point.x <= max(p1x, p2x)
            ):
                if p1y != p2y:
                    x_intersect = (point.y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x

                if p1x == p2x or point.x <= x_intersect:
                    inside = not inside

            p1x, p1y = p2x, p2y

        return inside

    def to_wkt(self) -> str:
        """Convert polygon to WKT string"""
        coords = []
        for point in self.points:
            coords.append(f"{point.x} {point.y}")

        return f"POLYGON(({', '.join(coords)}))"

    def distance_to(self, other: "Polygon") -> float:
        """Calculate the minimum distance between two polygons"""
        # Implement a basic version that checks all pairs of points
        min_distance = float("inf")

        for p1 in self.points:
            for p2 in other.points:
                dist = p1.distance_to(p2)
                if dist < min_distance:
                    min_distance = dist

        return min_distance

    def _do_segments_intersect(
        self, p1: Point, p2: Point, p3: Point, p4: Point
    ) -> bool:
        """Helper function to check if two line segments intersect"""

        # Function to check orientation of triplet (p, q, r)
        def orientation(p: Point, q: Point, r: Point) -> int:
            val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
            if val == 0:
                return 0  # collinear
            return 1 if val > 0 else 2  # clockwise or counterclockwise

        # Function to check if point q lies on segment pr
        def on_segment(p: Point, q: Point, r: Point) -> bool:
            return (
                q.x <= max(p.x, r.x)
                and q.x >= min(p.x, r.x)
                and q.y <= max(p.y, r.y)
                and q.y >= min(p.y, r.y)
            )

        # Find the four orientations
        o1 = orientation(p1, p2, p3)
        o2 = orientation(p1, p2, p4)
        o3 = orientation(p3, p4, p1)
        o4 = orientation(p3, p4, p2)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special Cases
        if o1 == 0 and on_segment(p1, p3, p2):
            return True
        if o2 == 0 and on_segment(p1, p4, p2):
            return True
        if o3 == 0 and on_segment(p3, p1, p4):
            return True
        if o4 == 0 and on_segment(p3, p2, p4):
            return True

        return False

    def intersects(self, other: "Polygon") -> bool:
        """Check if this polygon intersects with another polygon"""
        # Check if any edge of this polygon intersects with any edge of the other polygon
        n1 = len(self.points) - 1
        n2 = len(other.points) - 1

        # Check for edge intersections
        for i in range(n1):
            for j in range(n2):
                if self._do_segments_intersect(
                    self.points[i],
                    self.points[i + 1],
                    other.points[j],
                    other.points[j + 1],
                ):
                    return True

        # Check if one polygon is inside the other
        if self.contains_point(other.points[0]) or other.contains_point(self.points[0]):
            return True

        return False




    def intersection(self, other: "Polygon") -> Optional["Polygon"]:
        """Calculate the intersection of two polygons

        Note: This is a simplified implementation that works for convex polygons.
        A full implementation would require more complex algorithms like
        Sutherland-Hodgman or Weiler-Atherton.
        """
        if not self.intersects(other):
            return None

        # This is a placeholder for a more sophisticated implementation
        # For now, we'll identify intersection points and return a polygon if possible
        intersection_points = []

        # Find all intersection points between edges
        n1 = len(self.points) - 1
        n2 = len(other.points) - 1

        for i in range(n1):
            for j in range(n2):
                # Find intersection of line segments
                # This is a simplified check
                if self._do_segments_intersect(
                    self.points[i],
                    self.points[i + 1],
                    other.points[j],
                    other.points[j + 1],
                ):
                    
                    intersection_point = intersect_segments(self.points[i], self.points[i + 1], other.points[j], other.points[j + 1])
                    if intersection_point:
                        intersection_points.append(intersection_point)

                    # Add intersection point (simplified)
                    # In a real implementation, you would calculate the exact intersection point
                    # mid_x = (self.points[i].x + self.points[i + 1].x) / 2
                    # mid_y = (self.points[i].y + self.points[i + 1].y) / 2
                    # intersection_points.append(Point(mid_x, mid_y))

        # Add points from one polygon that are inside the other
        for point in self.points[:-1]:
            if other.contains_point(point):
                intersection_points.append(point)

        for point in other.points[:-1]:
            if self.contains_point(point):
                intersection_points.append(point)

        # If we have enough points, try to create a polygon
        if len(intersection_points) >= 3:
            # Sort points to create a valid polygon (this is a simplified approach)
            # A proper implementation would need a convex hull algorithm
            center = Point(
                sum(p.x for p in intersection_points) / len(intersection_points),
                sum(p.y for p in intersection_points) / len(intersection_points),
            )

            # Sort points based on angle from center
            def angle_from_center(p):
                return math.atan2(p.y - center.y, p.x - center.x)

            sorted_points = sorted(intersection_points, key=angle_from_center)
            return Polygon(sorted_points)

        return None

    def union(self, other: "Polygon") -> Optional["Polygon"]:
        """Calculate the union of two polygons

        Note: This is a simplified implementation that works for non-intersecting polygons.
        A full implementation would require more complex algorithms.
        """
        # Check if polygons are disjoint
        if not self.intersects(other):
            return None  # Would need to return a multipolygon in a full implementation

        # This is a placeholder for a more sophisticated implementation
        # A proper implementation would use techniques like:
        # - Binary space partitioning
        # - Constructive solid geometry
        # - Vatti clipping algorithm

        # For now, we'll return a simplified approximation
        # In a real implementation, you would calculate the exact union
        all_points = (
            self.points[:-1] + other.points[:-1]
        )  # Exclude the last points to avoid duplication

        # A proper implementation would need a convex hull algorithm
        center = Point(
            sum(p.x for p in all_points) / len(all_points),
            sum(p.y for p in all_points) / len(all_points),
        )

        # Sort points based on angle from center
        def angle_from_center(p):
            return math.atan2(p.y - center.y, p.x - center.x)

        sorted_points = sorted(all_points, key=angle_from_center)
        return Polygon(sorted_points)


class WKT:
    @staticmethod
    def from_wkt(wkt_string: str) -> Union[Point, Polygon, None]:
        """Parse WKT string into geometric objects"""
        wkt_string = wkt_string.strip()

        # Parse POINT
        if wkt_string.startswith("POINT"):
            match = re.search(
                r"POINT\s*\(\s*([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\s*\)", wkt_string
            )
            if match:
                x, y = float(match.group(1)), float(match.group(2))
                return Point(x, y)

        # Parse POLYGON
        elif wkt_string.startswith("POLYGON"):
            match = re.search(r"POLYGON\s*\(\s*\((.*?)\)\s*\)", wkt_string)
            if match:
                coords_str = match.group(1)
                coords_pairs = coords_str.split(",")
                points = []

                for pair in coords_pairs:
                    x, y = map(float, pair.strip().split())
                    points.append(Point(x, y))

                return Polygon(points)

        return None

    @staticmethod
    def to_wkt(geometry: Union[Point, Polygon]) -> str:
        """Convert geometric object to WKT string"""
        if isinstance(geometry, Point):
            return f"POINT({geometry.x} {geometry.y})"
        elif isinstance(geometry, Polygon):
            return geometry.to_wkt()
        else:
            raise TypeError("Unsupported geometry type")


# Example usage
if __name__ == "__main__":
    test_intersect_segments()
    # Create a square
    square = Polygon([Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)])

    # Create another polygon
    triangle = Polygon([Point(0.5, 0.5), Point(1.5, 0.5), Point(1, 1.5)])


    # Check if polygons intersect
    print(f"Polygons intersect: {square.intersects(triangle)}")

    # Calculate intersection
    intersection = square.intersection(triangle)
    if intersection:
        print(f"Intersection polygon: {WKT.to_wkt(intersection)}")
    else:
        print("No intersection found")

    test_intersect_segments() # Call the test function

    # Convert to WKT
    square_wkt = WKT.to_wkt(square)
    print(f"Square WKT: {square_wkt}")

    # Parse from WKT
    parsed_square = WKT.from_wkt(square_wkt)

    # Calculate center of mass
    center = square.center_of_mass()
    print(f"Center of mass: {center}")

    # Calculate distance between polygons
    distance = square.distance_to(triangle)
    print(f"Distance between polygons: {distance}")

    # Calculate union
    union = square.union(triangle)
    if union:
        print(f"Union polygon: {WKT.to_wkt(union)}")
    else:
        print("Couldn't calculate union")