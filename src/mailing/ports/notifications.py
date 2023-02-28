import abc


class EmailNotification(abc.ABC):
    @abc.abstractmethod
    def send(self, destination: str, message: str):
        ...
