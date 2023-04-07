from abc import ABC, abstractmethod

class IActuator(ABC):
    """
    The Actuator interface declares the start and stop method, used by the actuators.
    """

    @abstractmethod
    def Start() -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def Stop() -> None:
        """
        Detach an observer from the subject.
        """
        pass