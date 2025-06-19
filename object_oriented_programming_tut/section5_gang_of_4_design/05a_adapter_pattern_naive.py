"""
Adapter Pattern

allows incompatible interfaces between class to work together providing a wrapper that translates on interface into the other
"""
from abc import ABC, abstractmethod
class Video:
    def play(self):
        print("Playing video...")
        
    def stop(self):
        print("Stopping video...")
        
class Color():
    @abstractmethod
    def apply_filter(sef, video):
        pass
    
class BWFilter(Color):
    def apply(self, video):
        print("Applying BW filter...")

class MidnightFilter(Color):
    def apply(self, video):
        print("Applying Midnight filter...")
        
class VideoEditor:
    def __init__(self, video):
        self.video = video
        

    def apply_color(self, color:Color):
        color.apply(self.video)
    
video = Video()
video_editor = VideoEditor(video)
video_editor.apply_color(BWFilter())
video_editor.apply_color(MidnightFilter())

# Issue is if there is a 3rd party class for example rainbow, that does use the same methods, you can obviously not use the apply color method to that class
# See refactored solution
        
    