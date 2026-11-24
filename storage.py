from abc import ABC, abstractmethod

# Абстрактное хранилище заказов
class Storage(ABC):

    @abstractmethod
    def get_order(self, user_id):
        pass

    @abstractmethod
    def save_order(self, user_id, order):
        pass

    @abstractmethod
    def delete_order(self, user_id):
        pass