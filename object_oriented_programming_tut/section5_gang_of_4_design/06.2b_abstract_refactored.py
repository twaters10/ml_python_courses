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
    
class UIComponentFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_checkbox(self) -> CheckBox:
        pass
    
class WindowsUIComponentFactory(UIComponentFactory):
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_checkbox(self) -> CheckBox:
        return WindowsCheckBox()
    
class MacUIComponentFactory(UIComponentFactory):
    def create_button(self) -> Button:
        return MacButton()
    
    def create_checkbox(self) -> CheckBox:
        return MacCheckBox()
    
    
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
        
        
# Application classes: Refactored
class UserSettingsForm:
    def render(self, uicomponent_factory: UIComponentFactory):
        uicomponent_factory.create_button().render()
        uicomponent_factory.create_checkbox().render()
        

# Setup Application
os = OperatingSystemType.WINDOWS
ui_component_factory: UIComponentFactory

# Logic to determine which OS to render based on setup (add layer if new os system is add to above application (i.e. Linux))
if os == OperatingSystemType.WINDOWS:
    ui_component_factory = WindowsUIComponentFactory()
elif os == OperatingSystemType.MAC:
    ui_component_factory = MacUIComponentFactory()

UserSettingsForm().render(ui_component_factory)
        


