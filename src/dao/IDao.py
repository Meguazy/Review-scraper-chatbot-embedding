from abc import ABC, abstractmethod


class IDao(ABC):
    @abstractmethod
    def save(self, *args, **kwargs):
        """Salva i dati nel rispettivo database."""
        pass

    @abstractmethod
    def query(self, *args, **kwargs):
        """Esegue una query nel rispettivo database."""
        pass
