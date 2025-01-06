# pyPhyEngine - generator.py -> Generates a PhysicsRoom with random objects etc.
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

from . import models
import random

class PhysicsRoomGenerator:
    def __init__(
        self, 
        loop: bool = False,
        collision: bool = True
    ) -> None:
        """Generators a Random PhysicsRoom I guess lol

        Args:
            loop (bool, optional): Automatically generates another room if all balls aren't moving. Defaults to False.
            collision (bool, optional): Enables or disables collisions. Defaults to True.
        """
        self.PhysicsObjects = []
        self.Room = None
        self.collection = None
        self.loop = loop
        self.collision = collision
        
        self.create_objects()
        self.ObjectCollection()
        self.create_room()
    
    def create_objects(self):
        """Creates objects with random stats (idk what to call it)
        """
        for _ in range(random.randint(1,10)):
            Physic_Object = models.PhysicsObject(
                x=random.randint(1, 49),
                y=random.randint(5, 45),
                size=random.randint(30, 90),
                color=(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)),
                grav=random.randint(1, 2),
                bounce=(random.uniform(0.5, 1)),
                velocity_x=random.randint(-2, 2),
                velocity_y=random.randint(-1, 4),
                show_trajectory=True
            )
            self.PhysicsObjects.append(Physic_Object)
    
    def ObjectCollection(self) -> None:
        """Builds collection, nothing interesting lol
        """
        self.collection = ObjectCollection().build_collection(self.PhysicsObjects)
    
    def create_room(self):
        """Creates a physicsRoom for the Objects
        """
        self.Room = PhysicsRoom(
            record_video = False,
            OC = self.collection,
            debug = False,
            loop = self.loop,
            collision = self.collection
        ).render()