# pyPhyEngine - utils.py -> Stores varies utilities for calculations and more
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

import numpy as np

def generate_circle(
    x: int | float, 
    y: int | float, 
    r: int | float, 
    max_lines: int
) -> list[list[int]]:
    max_lines = max(3, max_lines)
    angles = np.linspace(0, 2*np.pi, max_lines, False) # angles from 0 to 2pi with amount of max_lines
    
    matrix = [
        list(x + r * np.cos(angles)),
        list(y + r * np.sin(angles))
    ]
    return matrix

def generate_rectangle(x1, y1, x2, y2):
    return [
        [x1, x2, x2, x2, x2, x1, x1, x1],
        [y1, y1, y1, y2, y2, y2, y2, y1]
    ]

def extract_physicsObjects(collection):
    return collection['PhysicsObject']