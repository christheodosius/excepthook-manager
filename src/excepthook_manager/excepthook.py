import abc

from excepthook_manager.exceptions import ExcepthookNotImplemented


class Excepthook(object):
    def __init__(self):
        super(Excepthook, self).__init__()
        self._is_blocking = False

    @property
    def is_blocking(self):
        return self._is_blocking

    @is_blocking.setter
    def is_blocking(self, value):
        self._is_blocking = bool(value)

    @abc.abstractmethod
    def execute(self, tb_type, value, tb):
        raise ExcepthookNotImplemented
