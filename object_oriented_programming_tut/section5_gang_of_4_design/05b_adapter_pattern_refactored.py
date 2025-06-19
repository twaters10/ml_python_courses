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

# 3rd party class Rainbow
class Rainbow:
    def setup(self):
        print("Setting up rainbow...")
    
    def update(self, video):
        print("Applying rainbow filter...")
        
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

# Solve this issue by converting the interface of the 3rd party classes to a different form using Adapter Pattern
# Create RainbowColor Class that is composed of the 3rd party rainbow class
class RainbowColor(Color):
    def __init__(self, rainbow: Rainbow):
        self._rainbow = Rainbow()  # protected and always = Rainbow()
        
    def apply(self, video):
        self._rainbow.setup()
        self._rainbow.update(video)
        
video = Video()
video_editor = VideoEditor(video)
video_editor.apply_color(BWFilter())
video_editor.apply_color(MidnightFilter())
video_editor.apply_color(RainbowColor(Rainbow()))
# This was done by composition, but can also be done via inheritance. Composition is prefered b/c its more modular.
