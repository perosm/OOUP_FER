from abc import ABC, abstractmethod
import numpy as np

class GeneratorStrategy(ABC): # ABC - Abstract Base Class
    """Abstract class"""
    @abstractmethod
    def generate(self):
        pass


# Concrete generator strategy implementations
class SequentialGeneratorStrategy(GeneratorStrategy):
    def __init__(self, start, end, step) -> None:
        self.start = start
        self.end = end
        self.step = step

    def generate(self):
        generatedNumbers = []
        for i in range(self.start, self.end, self.step):
            generatedNumbers.append(i)

        return generatedNumbers
    

class GaussianGeneratorStrategy(GeneratorStrategy):
    def __init__(self, mean: int, std: int, n: int) -> None:
        self.mean = mean
        self.std = std
        self.n = n

    def generate(self):
        generatedNumbers = []
        for i in range(self.n):
            generatedNumbers.append(round(np.random.normal(loc=self.mean, scale=self.std)))
        return generatedNumbers


class FibonacciGeneratorStrategy(GeneratorStrategy):
    def __init__(self, n: int) -> None:
        self.n = n

    def generate(self) -> list:
        first, second = 0, 1
        generatedNumbers = [first, second]
        for i in range(self.n - 2):
            next = first + second
            generatedNumbers.append(next)
            first = second
            second = next

        return generatedNumbers
            

class PercentileStrategy(ABC):
    @abstractmethod
    def calculate_percentile(self):
        pass


class PercentileNormalStrategy(PercentileStrategy):
    def __init__(self) -> None:
        pass

    def calculate_percentile(self, values: list, p: float):
        sorted_values = sorted(values)
        n_p = round(p * len(values) / 100 + 0.5)

        return sorted_values[max(0, min(n_p, len(values) - 1))]
    

class PercentileByInterpolationStrategy(PercentileStrategy):
    def __init__(self) -> None:
        pass

    def calculate_percentile(self, values: list, p: float):
        sorted_values = sorted(values)
        N = len(sorted_values)
        P_v = [(i - 0.5) * 100 / N for i in range(1, N + 1)]


        i = 0
        while i < N and P_v[i] < p:
            i += 1

        if i == 0:
            return sorted_values[0]
        elif i == N:
            return sorted_values[N-1]
        else:
            v_ip1 = sorted_values[i]
            v_i = sorted_values[i-1]
            return  v_i + N * (p - P_v[i-1]) * (v_ip1 - v_i) / 100

class DistributionTester:
    gs = None # generation strategy
    ps = None # percentile strategy
    def __init__(self, gs: GeneratorStrategy, ps: PercentileStrategy):
        self.gs = gs
        self.ps = ps

    def set_generator_strategy(self, newGs: GeneratorStrategy):
        self.gs = newGs

    def set_percentile_strategy(self, newPs: PercentileStrategy):
        self.ps = newPs

    def generate(self):
        return self.gs.generate()
    
    def calculate(self, values: list, p: float):
        return self.ps.calculate_percentile(values, p)
    
    def test(self, p):
        values = self.gs.generate()
        print(f'Generated numbers: {values}')
        print(f'Sorted generated numbers: {sorted(values)}')
        for p in percentiles:
            percentileCalc = self.ps.calculate_percentile(values, p)
            print(f'\tPercentile: {p}, Number: {percentileCalc}')


if __name__ == '__main__':
    generator = SequentialGeneratorStrategy(start=0, end=51, step=25)
    percentileCalc = PercentileNormalStrategy()
    ds = DistributionTester(generator, percentileCalc)
    percentiles = [10 * i for i in range(1, 10)]
    # Percentile Normal Strategy
    ds.test(percentiles)

    ds.gs = FibonacciGeneratorStrategy(10)
    ds.test(percentiles)

    ds.gs = GaussianGeneratorStrategy(10, 5, 10)
    ds.test(percentiles)

    # Percentile Interpolation Strategy
    #percentileCalc = PercentileByInterpolationStrategy()
    #print(percentileCalc.calculate_percentile([1, 10, 50], 80))
    ds.ps = PercentileByInterpolationStrategy()
    ds.gs = SequentialGeneratorStrategy(0, 51, 25)
    ds.test(percentiles)

    ds.gs = FibonacciGeneratorStrategy(10)
    ds.test(percentiles)

    ds.gs = GaussianGeneratorStrategy(10, 5, 10)
    ds.test(percentiles)