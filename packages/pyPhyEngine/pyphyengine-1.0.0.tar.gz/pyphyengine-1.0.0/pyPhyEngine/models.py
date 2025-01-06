# pyPhyEngine - models.py -> Stores object types and their functionality
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

from typing import(
    List
)

class PhysicsObject:
    def __init__(
        self, 
        x: int, 
        y: int,
        size: int | float = 50,
        grav: int | float = 1,
        fps: int = 60, 
        bounce: int = 1, 
        friction: int | float = 0.5,
        mass: int | float = 10,
        velocity_x: int | float = 0, 
        velocity_y: int | float = 0,
        border_x: List[int] = [0, 10],
        border_y: List[int] = [0, 30],
        color: str = "black",
        show_trajectory: bool = False,
        max_trajectory_iterations: int = 50,
    ) -> None:
        
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.size = size
        self.gravity = grav
        self.fps = fps
        self.bounce = bounce
        self.friction = friction
        self.mass = mass
        self.border_x = border_x
        self.border_y = border_y
        self.color = color
        self.show_trajectory = show_trajectory
        self.max_trajectory_iters = max_trajectory_iterations

        self.trajectory = {
            'x': [],
            'y': []
        }
        self.collisionObject = 0
        self.frame = 1
        self.total_frames = 0
    
    def tick(self) -> int | dict:
        """This script runs every time a new frame is rendered

        Returns:
            (int | dict): X-Position, Y-Position and trajectory dictionary
        """
        #       render -> if self.collision:
        self.velocity_y = round(self.velocity_y + (self.gravity / self.fps * self.frame), 2)
        
        self.y = self.validate_y_position(self.y - self.velocity_y)
        self.x = self.validate_x_position(self.x)
        
        if self.show_trajectory:
            self.validate_trajectory()
        
        self.frame += 1
        self.total_frames += 1
        return self.x, self.y, self.trajectory
    
    def validate_x_position(self, x: int) -> int:
        """
        This function performes certain calculations and\n
        conditions to validate the X-Position of the PhysicsObject

        Args:
            x (int): Current X-Position

        Returns:
            int: New X-Position after conditions and calculations
        """
        x_border_1 = self.border_x[0]
        x_border_2 = self.border_x[1]
        
        if x >= x_border_2 or x <= x_border_1:
            if x >= x_border_2:
                x = x_border_2
            else:
                x = x_border_1
            
            self.velocity_x = self.velocity_x * (-1) * self.bounce # right -> left | left -> right
        
        if self.y <= 0:
            # if velocity < 0.0000000001
            if abs(self.velocity_x) < 1e-9:
                self.velocity_x = 0
            
            self.velocity_x = self.velocity_x / (self.friction + 1)
            x = x + self.velocity_x
        else:
            x = x + self.velocity_x
        
        return x
    
    def validate_y_position(self, y: int) -> int:
        """This function performes certain calculations and\n
        conditions to validate the Y-Position of the PhysicsObject

        Args:
            y (int): Current Y-Position

        Returns:
            (int): New Y-Position
        """
        if y < self.border_y[0]:
            self.frame = 1
            self.velocity_y = round(-self.velocity_y * (self.bounce / 2), 2)
            y = self.border_y[0]
        
        if y > self.border_y[1]:
            y = self.border_y[1] # if it hits the ceiling, just stick to it lmao
            self.velocity_y = 0
        return y
    
    def validate_trajectory(self):
        """Appends current position to trajectory
        """
        if self.max_trajectory_iters:
            if len(self.trajectory['x']) > self.max_trajectory_iters:
                self.trajectory['x'].pop(0)
                self.trajectory['y'].pop(0)
        
        self.trajectory['x'].append(self.x)
        self.trajectory['y'].append(self.y)
    
    def get_data_string(self) -> str:
        """Returns a string with a lot of information about the ball

        Returns:
            str: Stats
        """
        return (
            f"x: {self.x}\n"
            f"y: {self.y}\n"
            f"x-velocity: {self.velocity_x}\n"
            f"y-velocity: {self.velocity_y}\n"
            f"frame: {self.frame}\n"
            f"gravity: {self.gravity}\n"
            f"applied_gravity: {self.applied_gravity}\n"
            f"total_frames: {self.total_frames}\n"
        )

class StaticObject:
    def __init__(
        self, 
        matrix: List[List[int]],
        color: str = "blue",
        fill_color: str = "blue"
    ) -> None:
        """A Static object that won't 
        
        move but can interact with other Objects

        Args:
            matrix (List[List[int]]): This declares the shape of the object
            color (str, optional): Color of the lines. Defaults to "blue".
            fill_color (str, optional): Fill Color. Defaults to "blue".
        """
        self.matrix = matrix
        self.color = color
        self.fill_color = fill_color