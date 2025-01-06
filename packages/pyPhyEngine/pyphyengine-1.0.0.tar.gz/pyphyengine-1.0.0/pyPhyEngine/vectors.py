# pyPhyEngine - vectors.py -> Calculates vectors and more
# Copyright (C) 2025  Florian, Floerianc on Github (https://www.github.com/floerianc)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import List

def get_vector_difference(
    A: List, 
    B: List
) -> tuple:
    """Returns the difference vector of two points

    Args:
        A (List): Point A
        B (List): Point B

    Returns:
        tuple: Vector between A and B
    """
    return [B[0] - A[0], B[1] - A[1]]

def extract_points(line: List) -> tuple:
    """Takes a line and returns the two ending points

    Args:
        line (List): the line :D

    Returns:
        tuple: Both ending points
    """
    return [line[0][0], line[0][1]], [line[1][0], line[1][1]]

def neutralize_points(*points):
    new_points = list()
    for point in enumerate(points):
        new_points.append([])
        
        for value in point[1]:
            new_points[point[0]].append(abs(value))
    
    return new_points

def point_collides_line(
    line: List[List], 
    Point: List
) -> bool:
    """Checks, if a given point sits on a given line

    Args:
        line (List[List]): The line
        Point (List): The point

    Returns:
        bool: True, if the point is on the line
    """
    # BUG: VECTORS DON'T WORK PROPERLY
    # FIXME: MAKE CODE BETTER
    
    A, B = extract_points(line)
    AB = get_vector_difference(A, B)
    
    APoint = get_vector_difference(A, Point)
    comparing_vectors = tuple(zip(AB, APoint))
    
    for value in comparing_vectors:
        divisor = value[0]
        if value[0] == 0: divisor = 1
        
        if value[1] / divisor >= 0 and value[1] / divisor <= 1:
            continue
        else:
            return False
    
    print("Collided with SO")
    return True