# pyPhyEngine - __init__.py -> Controls the graphing and generates ObjectCollection
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


import matplotlib.pyplot as plt
import os
from . import models
from . import generator
from . import renderer
from matplotlib.figure import Figure
from typing import Any

plt.style.use('_mpl-gallery')

class ObjectCollection:
    def check_class(
        self, 
        obj: Any
    ) -> bool | object | None:
        """Checks which class the object is connected to\n
        if the object exists within the given objectTypes\n
        then it returns True :D

        Args:
            obj (Any): Any object from this module

        Returns:
            bool | object | None: Either True, False, Object or None
        """
        objectTypes = {
            "PhysicsObject": models.PhysicsObject,
            "StaticObject": models.StaticObject
        }
        
        for objType in objectTypes:
            if isinstance(obj, objectTypes[objType]):
                return True, objType
        return False, None
    
    def build_collection(
        self, 
        *objects: Any
    ) -> dict:
        """Builds a dictionary seperating each object-type

        Returns:
            dict: dictionary with every object
        """
        collection = {}
        
        for l in objects:
            for obj in l:
                is_same_type, objectType = self.check_class(obj)
                
                if is_same_type:
                    try:
                        collection[objectType].append(obj)
                    except:
                        collection[objectType] = [obj]
        
        return collection

class PhysicsRoom:
    def __init__(
        self,
        OC: dict = None,
        collision: bool = True,
        KEGraphing: bool = False,
        tolerance: int | float = 0.25,
        loop: bool = False,
        record_video: bool = False,
        debug: bool = False,
    ) -> None:
        
        self.collection = OC
        self.collision = collision
        self.KEGraphing = KEGraphing
        self.tolerance = tolerance
        self.record_video = record_video
        self.debug = debug
        self.loop = loop
        
        self.is_running = False
        self.construct_room()
    
    def construct_room(self) -> dict:
        """Creates the borders of the room

        Returns:
            dict: dictionary of borders for room
        """
        left_xlim = []
        right_xlim = []
        lower_ylim = []
        upper_ylim = []
        fps = []
        
        for PhysicsObject in self.collection['PhysicsObject']:
            left_xlim.append(PhysicsObject.border_x[0])
            right_xlim.append(PhysicsObject.border_x[1])
            lower_ylim.append(PhysicsObject.border_y[0])
            upper_ylim.append(PhysicsObject.border_y[1])
            fps.append(PhysicsObject.fps)
        
        room_limits = {
            'xlim': [min(left_xlim), max(right_xlim)],
            'ylim': [min(lower_ylim), max(upper_ylim)],
            'fps': [max(fps)]
        }
        return room_limits
    
    def show_debug(self) -> None:
        """Prints debug information into terminal
        """
        os.system("cls")
        debug_string = ""
        
        for O in self.collection['PhysicsObject']:
            debug_string += (
                f"Object\n\n"
                f"X-Position: {O.x:2f}\n"
                f"Y-Position: {O.y:2f}\n"
                f"X-Velocity: {O.velocity_x:2f}\n"
                f"Y-Velocity: {O.velocity_y:2f}\n"
                f"Gravity: {O.gravity:2f}\n"
            )
        print(debug_string)
    
    def check_if_balls_moving(
        self, 
        fig: Figure
    ) -> None:
        """Checks if the balls are still moving or not

        Args:
            fig (Figure): Figure
        """
        for obj in self.collection['PhysicsObject']:
            if obj.velocity_x != 0:
                return False
            else:
                continue
        plt.close(fig)
        generator.PhysicsRoomGenerator(loop=True)
    
    def render(self):
        """Renders the plot with the given scatter and plot data and limits
        """
        self.is_running = True
        
        room_limits = self.construct_room()
        rendering = renderer.Renderer(
            room_limits['fps'][0], 
            self.loop, 
            self.collision, 
            self.record_video, 
            self.KEGraphing,
            self.collection
        )
        rendering.fig.tight_layout()
        
        def on_close(event) -> None:
            self.is_running = False
        rendering.fig.canvas.mpl_connect('close_event', on_close)
        
        if self.loop:
            self.check_if_balls_moving(rendering.fig)
        
        while self.is_running:
            rendering.initialize_render(room_limits)
            rendering.save_frame()
            plt.draw()
            
            if self.debug:
                self.show_debug()
            
            plt.pause(1 / room_limits['fps'][0])
        
        rendering.finish_video()

class KEGraphing:
    def __init__(self, objects: list[models.PhysicsObject]):
        self.objects = objects
        self.ylim = self.get_limit() / 2
    
    def get_kinetic_energy(self) -> list:
        ke_list = []
        
        for obj in self.objects:
            velocity = abs(obj.velocity_x) + abs(obj.velocity_y)
            ke = 1/2 * obj.mass * (velocity**2)
            ke_list.append(ke)
        return ke_list
    
    def get_limit(self) -> int:
        max_energies = []
        
        for obj in self.objects:
            max_energies.append(obj.mass * obj.gravity * obj.y)
        return max(max_energies)
    
    def get_axes(self):
        kes = self.get_kinetic_energy()
        x_axis = [f'PhysicsObject {i[0]}' for i in enumerate(self.objects)]
        y_axis = [ke for ke in kes]
        
        return {
            'x': x_axis,
            'y': y_axis,
        }