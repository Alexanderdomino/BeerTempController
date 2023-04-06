from abc import ABC, abstractmethod
from Interfaces.ISubject import ISubject

class IObserver(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: ISubject) -> None:
        """
        Receive update from subject.
        """
        pass