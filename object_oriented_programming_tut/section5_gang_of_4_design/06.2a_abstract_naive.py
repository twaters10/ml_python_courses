"""
Abstract Factory Pattern is a creational design pattern that proides an interface for creating families of related objects without specifying 
their concrete classes. Promotes encapsulation and allowing for the creation of object families that can vary independently.
"""
from enum import Enum
from math import *
from abc import ABC, abstractmethod

# UI Framework

class OperatingSystemType(Enum):
    WINDOWS = "WINDOWS"
    MAC = "MAC"

class UIComponent(ABC):
    @abstractmethod
    def render(self):
        pass

class CheckBox(UIComponent):
    @abstractmethod
    def on_select(self):
        pass
    
class Button(UIComponent):
    @abstractmethod
    def on_click(self):
        pass
    
# Windows components
class WindowsButton(Button):
    def render(self):
        print("Rendering Windows Button")
        
    def on_click(self):
        print("Windows Button Clicked")
        
class WindowsCheckBox(CheckBox):
    def render(self):
        print("Rendering Windows CheckBox")
        
    def on_select(self):
        print("Windows CheckBox Selected")
        
# Mac Components
class MacButton(Button):
    def render(self):
        print("Rendering Mac Button")
        
    def on_click(self):
        print("Mac Button Clicked")
        
class MacCheckBox(CheckBox):
    def render(self):
        print("Rendering Mac CheckBox")
        
    def on_select(self):
        print("Mac CheckBox Selected")
        
        
# Application classes: Issue is we will need to create conditionals for every UI created, gross!
class UserSettingsForm:
    def render(self, os: OperatingSystemType):
        if os == OperatingSystemType.WINDOWS:
            WindowsCheckBox().render()
            WindowsButton().render()
        elif os == OperatingSystemType.MAC:
            MacCheckBox().render()
            MacButton().render()

# Using above solution
os = OperatingSystemType.MAC
user_settings_form = UserSettingsForm()
user_settings_form.render(os)
        

