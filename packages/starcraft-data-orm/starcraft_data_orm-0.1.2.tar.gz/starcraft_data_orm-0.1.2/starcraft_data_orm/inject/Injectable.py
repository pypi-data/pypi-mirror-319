from abc import ABC, abstractmethod
from collections import defaultdict


class Injectable(ABC):
    @classmethod
    @property
    @abstractmethod
    def __tableschema__(cls):
        """Return the schema name. Must be implemented by subclasses."""
        pass

    @classmethod
    @abstractmethod
    async def process(cls, replay, session):
        """Must be implemented by subclasses."""
        pass

    @classmethod
    def get_data(cls, obj):
        parameters = defaultdict(lambda: None)
        for variable, value in vars(obj).items():
            print(f"Processing variable: {variable}, value: {value}")
            if variable in cls.columns:
                parameters[variable] = value
        print(f"Extracted parameters: {parameters}")
        return parameters
