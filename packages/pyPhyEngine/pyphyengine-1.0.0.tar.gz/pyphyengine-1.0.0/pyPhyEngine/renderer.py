# pyPhyEngine - renderer.py -> Renders objects etc. on graph
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
import numpy as np
from . import video
from . import collider
from . import models
from typing import Any
from matplotlib.axes import Axes
from matplotlib.figure import Figure

class Renderer:
    # TODO: ADD DOCS
    def __init__(
        self,
        fps: int = 60,
        loop: bool = False,
        collision: bool = True,
        recorder: bool = False,
        KEGraphing: bool = False,
        collection: dict = None
    ) -> None:
        
        self.fps = fps
        
        self.loop = loop
        self.collision = collision
        self.KEGraphing = KEGraphing
        self.collection = collection
        
        self.recorder = recorder
        self.collider = collision
        
        self.fig, self.ax = self.setup()
        self.initialized_objects = dict()
    
    def setup(self) -> Figure | Axes:
        """Initiates the recorded and collider if the users
        
        wishes to enable both of them

        Returns:
            Figure | Axes: Returns Figure and Axis for the script
            
            which runs this.
        """
        if self.recorder:
            self.recorder = video.VideoRecorder(self.fps, delete_temp=True)
        
        if self.collider:
            self.collider = collider.Collider(0.25)
        
        if self.KEGraphing:
            self.KEGraphing = KEGraphing(self.collection['PhysicsObject'])
            f, a = plt.subplots(2, 1, figsize=[10, 8], dpi=80)
        else:
            f, a = plt.subplots(figsize=[10, 8], dpi=80)
        return f, a
    
    def save_frame(self):
        """If the recorded is enabled, it will try to save the current frame
        """
        if self.recorder:
            self.recorder.save_frame(self.fig)
    
    def render_object(self, obj: Any, axis: Axes) -> None:
        """Renders each object.
        
        The ObjectType matters in the rendering process

        Args:
            obj (Any): The Object that should be rendered
        """
        if isinstance(obj, models.PhysicsObject):
            x, y, trajectories = obj.tick()
            
            if obj not in self.initialized_objects:
                self.initialized_objects[obj] = {
                    'scatter': axis.scatter(x, y, s=obj.size, c=obj.color),
                    'plot': axis.plot([], [], c=obj.color)[0] # get first plot of initialized plot
                }
            
            else:
                if trajectories:
                    self.initialized_objects[obj]['plot'].set_data(trajectories['x'], trajectories['y'])
                self.initialized_objects[obj]['scatter'].set_offsets(np.c_[x, y])
        
        elif isinstance(obj, models.StaticObject):
            mSO = obj.matrix # matrix of object
            
            if obj not in self.initialized_objects: # if SO wasn't initialized yet
                self.initialized_objects[obj] = { # appends object to initialized objects
                    "scatter": axis.scatter(mSO[0], mSO[1], color=obj.color),
                    "line": axis.plot(mSO[0], mSO[1], color=obj.color)[0],
                    "fill": axis.fill(mSO[0], mSO[1], color=obj.fill_color, alpha=0.5)[0],
                }
            
            else: # if it's already there, just set the data
                self.initialized_objects[obj]["scatter"].set_offsets(np.c_[mSO[0], mSO[1]])
                self.initialized_objects[obj]["line"].set_data(mSO[0], mSO[1])
    
    def render_all_objects(
        self,
        collection: dict,
        axis: Axes
    ) -> None:
        """Renders every object declared in collection

        Args:
            collection (dict): Collection with every object
        """
        for objectType in collection:
            for obj in collection[objectType]:
                self.render_object(obj, axis)
    
    def set_axis_template(
        self, 
        axis: Axes, 
        room_limits: dict
    ) -> None:
        axis.axhline(room_limits['ylim'][0], color='black', linewidth=5)
        axis.set_xlim(room_limits['xlim'][0], room_limits['xlim'][1])
        axis.set_ylim(room_limits['ylim'][0], room_limits['ylim'][1])
    
    def draw_kinetic_energy(self, axis: Axes):
        axis.cla()
        
        axes = self.KEGraphing.get_axes()
        axis.bar(axes['x'], axes['y'], color='yellow')
        axis.set_ylim(0, self.KEGraphing.ylim)
    
    def initialize_render(
        self,
        room_limits: dict
    ) -> None:
        
        if self.KEGraphing:
            # sets limits for axis 0 and renders all objects
            self.set_axis_template(self.ax[0], room_limits)
            self.render_all_objects(self.collection, self.ax[0])
            
            # draws bar graph for KE
            self.draw_kinetic_energy(self.ax[1])
        else:
            self.set_axis_template(self.ax, room_limits)
            self.render_all_objects(self.collection, self.ax)
        
        if self.collision:
            for iteration in range(len(self.collection['PhysicsObject'])):
                self.collider.get_objects(self.collection) # gets all objects
                
                physicsObject = self.collider.extract_current_object(iteration)
                collided = self.collider.check_collides(physicsObject) # collide between current and all other
                
                if collided:
                    break # I hate this 
    
    def finish_video(self):
        """If the recorder is enabled, it will render the whole video
        """
        if self.recorder:
            self.recorder.render_video()