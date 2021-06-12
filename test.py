import logging
from settings import Settings
from sip import Adapter
from gui import Gui, GuiLogger

logging.basicConfig(filename="sipclient.log", level=logging.INFO)

GuiLogger.guiLogger = GuiLogger.GuiLogger()
__settings__ = Settings.Settings(GuiLogger.guiLogger)
__session__ = Adapter.Adapter(__settings__)

gui = Gui.Gui(__session__)
gui.display()
