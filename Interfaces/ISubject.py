from abc import ABC, abstractmethod

class ISubject(ABC):
    """
    Defines the Subject Interface
    """

    @abstractmethod
    def attach(self, observer: 'IObserver') -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: 'IObserver') -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass