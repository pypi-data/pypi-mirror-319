# pyPhyEngine - collider.py -> Checks for collisions and reacts accordingly
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

import math
from . import vectors
from .models import(
    PhysicsObject,
    StaticObject
)
from typing import(
    Any,
    Literal
)
from copy import deepcopy

class Collider:
    def __init__(self, tolerance: int | float) -> None:
        """Initializes Collider object

        Args:
            tolerance (int | float): Tolerance value for collisions
                                    DOESNT WORK YET LMAOOO
        """
        self.objects = {
            'PhysicsObject': [],
            'StaticObject': []
        }
        self.tolerance = tolerance
    
    def get_objects(
        self, 
        collection: dict
    ) -> None:
        self.objects = {
            'PhysicsObject': [],
            'StaticObject': []
        }
        
        try:
            for O in collection['PhysicsObject']:
                self.objects['PhysicsObject'].append(O)
        except:
            pass # No Physics Objects found
        
        try:
            for O in collection['StaticObject']:
                self.objects['StaticObject'].append(O)
        except:
            pass # No Static Objects in collection
    
    def extract_current_object(
        self, 
        iteration: int
    ) -> PhysicsObject:
        """Returns an PhysicsObject from collection

        Args:
            iteration (int): which item gets popped from list

        Returns:
            PhysicsObject: PhysicsObject
        """
        return self.objects['PhysicsObject'].pop(iteration)
    
    def check_collides_physicsObject(
        self, 
        object1: PhysicsObject, 
        physicsObject: PhysicsObject
    ) -> tuple[bool] | PhysicsObject:
        """Checks if two PhysicsObjects collide

        Args:
            object1 (PhysicsObject): First PhysicsObject
            physicsObject (PhysicsObject): Second PhysicsObject

        Returns:
            tuple[bool] | PhysicsObject: Returns True if collide and PhysicsObjects that collide
        """
        
        o1_x = object1.x
        o1_y = object1.y
        
        o2_x = physicsObject.x
        o2_y = physicsObject.y
        
        distance = math.sqrt((o1_x - o2_x)**2 + (o1_y - o2_y)**2)
        if distance < 0.2 and distance >= 0:
            return (True, object1, physicsObject)
    
    def lines_staticObject(
        self, 
        staticObject: StaticObject
    ) -> list:
        """Returns each line of a StaticObject

        Args:
            staticObject (StaticObject): The StaticObject

        Returns:
            list: List of lines that make up the StaticObject
        """
        lines = list()
        matrix = deepcopy(staticObject.matrix)
        
        while len(matrix[0]) >= 2:
            line = list()
            
            for _ in range(2):
                x = matrix[0].pop(0)
                y = matrix[1].pop(0)
                
                line.append((x, y))
            
            lines.append(line)
        return lines
    
    def check_collides_staticObject(
        self, 
        object1: PhysicsObject, 
        staticObject: StaticObject
    ) -> bool:
        """Checks if a PhysicsObject collides with any staticObjects

        Args:
            object1 (PhysicsObject): PhysicsObject
            staticObject (StaticObject): StaticObject

        Returns:
            bool: Returns True if they collide
        """
        # I HAVE NO CLUE WHAT I AM DOING
        # quick definition:
        #   line -> [(x1, y1), (x2, y2)]
        #   a line consists of two points that are connected 👍
        
        lines = self.lines_staticObject(staticObject)

        for line in lines:
            stats = {
                'A': {
                    'x': line[0][0],
                    'y': line[0][1]
                },
                'B': {
                    'x': line[1][0],
                    'y': line[1][1],
                }
            }
            
            if vectors.point_collides_line(line, [object1.x, object1.y]):
                return True
    
    def check_collides(
        self, 
        object1: PhysicsObject
    ) -> bool:
        """Checks if a PhysicsObject collides 
        
        with any other Objects in the PhysicsRoom

        Args:
            object1 (PhysicsObject): The PhysicsObject
        """
        for po in self.objects['PhysicsObject']:
            conclusion = self.check_collides_physicsObject(object1, po)
            
            if conclusion:
                self.collide(conclusion[1], conclusion[2]) # conclusion[1] -> object1   conclusion[2] -> object2
                return True
        
        for so in self.objects['StaticObject']:
            conclusion = self.check_collides_staticObject(object1, so)
            
            if conclusion:
                self.collide(object1, None)
                return True
    
    def calculate_velocities(self, obj1, obj2) -> dict[str, dict[str, int | float]]:
        # TODO: ADD DOCS :D
        # FIXME: MASS DOESN'T WORK AHSJIHDSGDJHSKGcnx
        # FOR NOW: TEMPORARY SOLUTION 👍👍
        
        def calculate_velocity(m1, m2, v1, v2, reverse=False):
            if reverse:
                return (2 * m1) / (m1 + m2) * v1 + (m2 - m1) / (m1 + m2) * v2
            return (m1 - m2) / (m1 + m2) * v1 + (2 * m2) / (m1 + m2) * v2
        
        velocities = {
            'object1': {
                'x': calculate_velocity(obj1.mass, obj2.mass, obj1.velocity_x, obj2.velocity_x),
                'y': calculate_velocity(obj1.mass, obj2.mass, obj1.velocity_y, obj2.velocity_y),
            },
            'object2': {
                'x': calculate_velocity(obj2.mass, obj1.mass, obj1.velocity_x, obj2.velocity_x, reverse=True),
                'y': calculate_velocity(obj2.mass, obj1.mass, obj1.velocity_y, obj2.velocity_y, reverse=True),
            },
        }
        return velocities
    
    def collide(
        self, 
        object1: PhysicsObject, 
        object2: PhysicsObject | None
    ) -> None:
        """Changes the PhysicsObjects' velocity on collision

        Args:
            object1 (PhysicsObject): First Object
            object2 (PhysicsObject | None): Second Object
        """
        if not object2:
            object1.velocity_x = -object1.velocity_x * object1.bounce
            object1.velocity_y = -object1.velocity_y * object1.bounce
        
        else:
            velocities = self.calculate_velocities(object1, object2)
            
            object1.velocity_x = velocities['object1']['x']
            object1.velocity_y = velocities['object1']['y']
            object2.velocity_x = velocities['object2']['x']
            object2.velocity_y = velocities['object2']['y']