import logging

__logger__ = logging.getLogger(__name__)

class GuiLogger:
    def __init__(self):
        self.loggerFunc = None

    def init(self, p_loggerFunc):
        self.loggerFunc = p_loggerFunc

    def log(self, msg : str):
        if self.loggerFunc == None:
            print(msg)
            __logger__.warning("GuiLogger not initiated!")
            __logger__.warning("GuiLogger: " + msg)
        else:
            self.loggerFunc(msg)
    
guiLogger = None
