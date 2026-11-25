
from abc import ABC, abstractmethod


class ProductionStrategy(ABC):

    @abstractmethod
    def calculate(self, total_input, total_output, total_wastage):
        pass


class YieldStrategy(ProductionStrategy):

    def calculate(self, total_input, total_output, total_wastage):
        if total_input <= 0:
            return 0

        return (total_output / total_input) * 100


class WastageStrategy(ProductionStrategy):

    def calculate(self, total_input, total_output, total_wastage):
        if total_input <= 0:
            return 0

        return (total_wastage / total_input) * 100
