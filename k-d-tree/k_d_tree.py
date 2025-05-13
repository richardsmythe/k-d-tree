# take points, sort them by axis, spluit by median, recurse for sub branches of tree
import math
from typing import List, Tuple, Optional
import pprint

pp = pprint.PrettyPrinter(indent=4)
Point = Tuple[float, float]
DIMENSIONS = [0, 1] 

def straight_line_distance(point1: Point, point2: Point) -> float:
    x1, y1 = point1
    x2, y2 = point2
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx * dx + dy * dy)

def build_kdtree(points, depth=0):
    n = len(points)
    if n <= 0:
        return None
    axis = DIMENSIONS[depth % len(DIMENSIONS)]
    sorted_points = sorted(points, key=lambda point: point[axis])
    median_idx = n // 2
    median_point = sorted_points[median_idx]

    left_points = [sorted_points[i] for i in range(median_idx)]
    right_points = [sorted_points[i] for i in range(median_idx + 1, n)]

    node = {
        "point": median_point,
        "left": build_kdtree(left_points, depth + 1),
        "right": build_kdtree(right_points, depth + 1),
    }

    return node

def kdtree_closest_point(root, target_point, depth=0, best_point=None):
    if root is None:
        return best_point

    axis = DIMENSIONS[depth % len(DIMENSIONS)]
    current_point = root['point']

    distance_to_current = straight_line_distance(target_point, current_point)
    best_distance = straight_line_distance(target_point, best_point) if best_point else float('inf')


    if best_point is None or distance_to_current < best_distance:
        best_point = current_point
        best_distance = distance_to_current

    target_value = target_point[axis]
    current_value = current_point[axis]

    if target_value < current_value:
        near_branch = root['left']
        far_branch = root['right']
    else:
        near_branch = root['right']
        far_branch = root['left']

    best_point = kdtree_closest_point(near_branch, target_point, depth + 1, best_point)

    distance_to_splitting_line = abs(target_value - current_value)

    if distance_to_splitting_line < best_distance:
        best_point = kdtree_closest_point(far_branch, target_point, depth + 1, best_point)

    return best_point


if __name__ == "__main__":
    points = [
        (0.0, 0.0),
        (1.2, 3.4),
        (2.5, 1.1),
        (4.8, 2.9),
        (3.3, 3.7),
        (5.1, 0.4),
        (0.9, 2.2),
        (2.7, 4.4),
        (3.6, 1.8),
        (4.2, 3.3),
        (1.5, 0.6),
        (2.0, 3.1),
        (3.9, 0.9),
        (1.8, 2.6),
        (0.4, 1.9),

    ]
    new_point = (14.0,9.0)

    kdtree = build_kdtree(points)
    closest_point = kdtree_closest_point(kdtree, new_point)
    print(f"closest point to {new_point} is {closest_point}")
