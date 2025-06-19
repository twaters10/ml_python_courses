# Observer Pattern Refactored Solution

from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update() -> None:
        pass

class Sheet2(Observer):
    def __init__(self, data_source):
        self.total = 0
        self.data_source = data_source
        
    def update(self) -> None:
        self.total = self.calculate_total(self.data_source.values)
        
    def calculate_total(self, values: list[float]):
        sum = 0
        for value in values:
            sum += value
        self.total = sum
        print(f"New Total is {sum}")
        return self.total
    
class BarChart(Observer):
    def __init__(self, data_source):
        self.data_source = data_source    

    def update(self):
        print("Rendering bar chart")
    
class Subject:
    def __init__(self):
        self.observers: list[Observer] = []
        
    def add_observer(self, observer: Observer) -> None:
        self.observers.append(observer)
        
    def remove_observer(self, observer: Observer) -> None:
        self.observers.remove(observer)
        
    def notify_observers(self) -> None:
        for observer in self.observers:
            observer.update()
        
class DataSource(Subject):
    def __init__(self):
        super().__init__()
        self._values: list[float] = []
        
    @property
    def values(self) -> list[float]:
        return self._values
    
    @values.setter
    def values(self, values: list[float]) -> None:
        self._values = values
        super().notify_observers()
            
                    
data_source = DataSource()
sheet2 = Sheet2(data_source)
bar_chart = BarChart(data_source)

data_source.add_observer(sheet2)
data_source.add_observer(bar_chart)
print(data_source.values)

data_source.values = [1,2,3,4,5]

# Push Pull Notification Styles:
    # Push Style:
# Subject pushes the changes to the observer
# Pull Style:
    # If each observer needs a different set of values a pull style can be utilized
    # Concrete observer will store a reference to the concrete subject


