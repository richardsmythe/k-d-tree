from dataclasses import dataclass
import math
from typing import List, Optional


@dataclass
class Point:
    x: float
    y: float

    def __getitem__(self, index: int) -> float:
        return (self.x, self.y)[index]

    def __repr__(self):
        return f"({self.x}, {self.y})"

@dataclass
class KDTreeNode:
    point: Point
    left: Optional['KDTreeNode'] = None
    right: Optional['KDTreeNode'] = None

DIMENSIONS = [0, 1]

def get_coord(point: Point, axis: int) -> float:
    return point.x if axis == 0 else point.y

def straight_line_distance(point1: Point, point2: Point) -> float:
    dx = point1.x - point2.x
    dy = point1.y - point2.y
    return dx * dx + dy * dy

def build_kdtree(points: List[Point], depth=0) -> Optional[KDTreeNode]:
    if not points:
        return None
    axis = DIMENSIONS[depth % len(DIMENSIONS)]
    sorted_points = sorted(points, key=lambda point: get_coord(point, axis))
    median_idx = len(sorted_points) // 2
    median_point = sorted_points[median_idx]
    return KDTreeNode(
        point=median_point,
        left=build_kdtree(sorted_points[:median_idx], depth + 1),
        right=build_kdtree(sorted_points[median_idx + 1:], depth + 1)
    )

def kdtree_1_nearest_neighbour(root: Optional[KDTreeNode], 
                         target_point: Point, 
                         depth=0, 
                         best_point: Optional[Point] = None) -> Optional[Point]:
    if root is None:
        return best_point

    axis = DIMENSIONS[depth % len(DIMENSIONS)]

    distance_to_current = straight_line_distance(target_point, root.point)
    best_distance = float('inf') if best_point is None else straight_line_distance(target_point, best_point)

    if best_point is None or distance_to_current < best_distance:
        best_point = root.point
        best_distance = distance_to_current

    target_value = get_coord(target_point, axis)
    current_value = get_coord(root.point, axis)

    if target_value < current_value:
        near_branch = root.left
        far_branch = root.right
    else:
        near_branch = root.right
        far_branch = root.left

    best_point = kdtree_1_nearest_neighbour(near_branch, target_point, depth + 1, best_point)

    if abs(target_value - current_value) < best_distance:
        best_point = kdtree_1_nearest_neighbour(far_branch, target_point, depth + 1, best_point)

    return best_point  
    

if __name__ == "__main__":
    points = [
        Point(2.0, 4.0),
        Point(6.0, 15.0),
        Point(3.0, 4.0),
        Point(15.0, 13.0),
        Point(17.0, 15.0),
        Point(3.0, 2.0),
        Point(14.0, 19.0),
    ]
    new_point = Point(2.0, 3.0)

    kdtree = build_kdtree(points)

    closest_point = kdtree_1_nearest_neighbour(kdtree, new_point)

    print(f"closest point to {new_point} is {closest_point}")    

