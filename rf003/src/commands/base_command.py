from abc import ABC, abstractmethod

class BaseCommannd(ABC):
    @abstractmethod
    def ejecutar(self): # pragma: no cover
        raise NotImplementedError("Please implement in subclass")