import threading
import time
import logging

__logger__ = logging.getLogger(__name__)

class GuiLogger:
    def __init__(self):
        self.loggerFunc = None

    def init(self, p_loggerFunc):
        self.loggerFunc = p_loggerFunc

    def log(self, log : str):
        if self.loggerFunc == None:
            print(log)
            __logger__.warning("GuiLogger not initiated!")
        else:
            self.loggerFunc(log)
    
guiLogger = None
