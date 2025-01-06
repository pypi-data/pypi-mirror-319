# pyPhyEngine - video.py -> Saves each frame from graph and renders full video
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

import os
import cv2
from natsort import natsorted, ns
from matplotlib.figure import Figure

class VideoRecorder:
    def __init__(
        self, 
        fps: int,
        video_path: str = '.\\',
        delete_temp: bool = False
    ) -> None:
        """Initializes the VideoRecorder Class

        Args:
            fps (int): Frames per Second that will be recorded
            video_path (str, optional): Path to the video. Defaults to '.\\'.
            delete_temp (bool, optional): Deletes every individual frame that was saved. Defaults to False.
        """
        
        self.frame_count = 0
        self.images_path = f"{os.path.dirname(__file__)}\\tmp\\"
        self.video_path = video_path
        self.fps = fps
        self.delete_temp = delete_temp
        
        if self.delete_temp:
            self.delete_tmp()
    
    def delete_tmp(self) -> None:
        """Deletes every individual frame in the temporary folder
        """
        for file in os.listdir(self.images_path):
            os.remove(os.path.join(self.images_path, file))
    
    def save_frame(self, plot: Figure) -> None:
        """Saves the current plot as a .png image

        Args:
            plot (Figure): Current plot/graph
        """
        plot.savefig(f'{self.images_path}{self.frame_count}.png')
        self.frame_count += 1
    
    def render_video(self) -> None:
        """Renders the whole video and saves it
        """
        images = []
        
        for img in os.listdir(self.images_path): # appends all images from path to list
            if img.endswith(".png"):
                images.append(img)
        
        frame = cv2.imread(os.path.join(self.images_path, images[1])) # Reads the first image
        height, width, layers = frame.shape # Saves the dimensions of the first image
        
        # VideoWriter_fourcc(*'DIVX) -> codec
        # FPS
        # resolution
        video = cv2.VideoWriter(
            f'{self.video_path}video_name.avi', 
            cv2.VideoWriter_fourcc(*'DIVX'), 
            self.fps, 
            (width, height)
        )
        
        for image in natsorted(images, alg=ns.IGNORECASE): # natural sorted version of images
            print(f"adding {image}")
            video.write(cv2.imread(os.path.join(self.images_path, image))) # adds image to video
        
        video.release()
        cv2.destroyAllWindows() # finalizes video 🤑🤑🤑
        self.delete_tmp()