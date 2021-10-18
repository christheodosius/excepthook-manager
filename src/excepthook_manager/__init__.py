"""
ExcepthookManager implementation. Copyright (c) Chris Theodosius 2021
"""
import sys

from excepthook_manager.excepthook import Excepthook
from excepthook_manager import exceptions


class ExcepthookManager(object):
    """
    Manager of Excephook classes. Handles the registering and de-registering of Excepthooks.
    """
    excepthooks = []

    @classmethod
    def register_excepthook(cls, excepthook):
        """
        Register an excepthook to be executed when an exception is caught.
        :param excepthook :type: Excephook instance
        :return:
        """
        if not isinstance(excepthook, Excepthook):
            raise exceptions.InvalidExcepthook
        if excepthook not in cls.excepthooks:
            cls.excepthooks.append(excepthook)

    @classmethod
    def deregister_excepthook(cls, excepthook):
        """
        De-register an excepthook
        :param excepthook:
        :return:
        """
        if excepthook in cls.excepthooks:
            cls.excepthooks.remove(excepthook)

    @classmethod
    def _sys_excepthook(cls, tb_type, value, tb):
        """
        Override of the _sys_excepthook
        :return:
        """
        # Call all the registered excepthooks
        cls._call_excepthook(tb_type, value, tb)
        return sys.__excepthook__(tb_type, value, tb)

    @classmethod
    def _maya_excepthook(cls, tb_type, value, tb, detail=2):
        """
        Override of the _maya_excepthook
        :return:
        """
        # Call all the registered excepthooks
        cls._call_excepthook(tb_type, value, tb)
        # Maya utils will import as this excepthook will only be registered when in the context of maya
        import maya.utils
        return maya.utils.formatGuiException(tb_type, value, tb, detail)

    @classmethod
    def _call_excepthook(cls, tb_type, value, tb):
        """
        Iterate through all the none blocking excepthooks and execute them
        :return:
        """
        for excepthook in cls.excepthooks:
            if excepthook.is_blocking:
                continue
            excepthook.execute(tb_type=tb_type, value=value, tb=tb)

    @classmethod
    def setup(cls):
        """
        Override the default excepthooks
        :return:
        """
        sys.excepthook = cls._sys_excepthook
        try:
            import maya.utils
            maya.utils._guiExceptHook = cls.maya_excepthook
        except ImportError:
            pass


ExcepthookManager.setup()
if __name__ == '__main__':
    class TestExceptHook(Excepthook):
        def execute(self, tb_type, value, tb):
            print("First")


    ExcepthookManager.register_excepthook(TestExceptHook())
    raise Exception
