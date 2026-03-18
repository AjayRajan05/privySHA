from abc import ABC, abstractmethod


class BaseAdapter(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass