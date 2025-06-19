# Observer Pattern Naive Solution

class Sheet2:
    def __init__(self):
        self.total = 0
        
    def calculate_total(self, values: list[float]):
        sum = 0
        for value in values:
            sum += value
        self.total = sum
        print(f"New Total is {sum}")
        return self.total
    
class BarChart:
    def render(self, values:list[float]):
        print("Rendering bar chart")
        
class DataSource:
    def __init__(self):
        self._values: list[float] = []
        self.dependents: list[object] = []
        
    @property
    def values(self) -> list[float]:
        return self._values
    
    @values.setter
    def values(self, values: list[float]) -> None:
        self._values = values
        
        # Update dependicies
        for dependent in self.dependents:
            if isinstance(dependent, Sheet2):
                dependent.calculate_total(values)
            elif isinstance(dependent, BarChart):
                dependent.render(values)
    
    def add_dependent(self, dependent: object) -> None:
        self.dependents.append(dependent)
        
    def remove_dependent(self, dependent: object) -> None:
        self.dependents.remove(dependent)
        
sheet2 = Sheet2()
bar_chart = BarChart()      
data_source = DataSource()
# Cleaner to apply a method to add or remove dependencies rather than doing that ouside the class
# data_source.dependents.append(Sheet2()) 
# data_source.dependents.append(BarChart())

data_source.add_dependent(sheet2)
data_source.add_dependent(bar_chart)
data_source.values = [1, 2, 3, 4.1]

data_source.remove_dependent(bar_chart)
data_source.values = [1, 2, 3, 4.1]
