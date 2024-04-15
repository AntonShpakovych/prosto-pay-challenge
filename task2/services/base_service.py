from abc import ABC

from task2.repositories.base_repository import BaseRepository


class BaseService(ABC):
    """
    An abstract base class for service classes.
    """
    def __init__(self, repository: BaseRepository):
        self.repository = repository
