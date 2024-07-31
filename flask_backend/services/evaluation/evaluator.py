from abc import ABC, abstractmethod
from typing import List, Union

class EvaluationStrategy(ABC):
    @abstractmethod
    def evaluate(self, reference_sentences: Union[str, List[str]], 
                 hypothesis_sentences: Union[str, List[str]], 
                 source_sentences: Union[str, List[str]] = None) -> float:
        pass

class Evaluator:
    def __init__(self, strategy: EvaluationStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: EvaluationStrategy):
        self.strategy = strategy

    def evaluate(self, reference_sentences: Union[str, List[str]], 
                 hypothesis_sentences: Union[str, List[str]], 
                 source_sentences: Union[str, List[str]] = None) -> float:
        return self.strategy.evaluate(reference_sentences, hypothesis_sentences, source_sentences)