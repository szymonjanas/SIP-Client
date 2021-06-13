import logging
from settings import Settings
from sip import Adapter
from gui import Gui, GuiLogger
from datetime import datetime

logging.basicConfig(filename="sipclient.log", level=logging.DEBUG)
__logger__ = logging.getLogger(__name__)

now = datetime.now()
timestamp = datetime.timestamp(now)
__logger__.info("\r\nSIP Client starts at: " + str(timestamp) + '\r\n')

GuiLogger.guiLogger = GuiLogger.GuiLogger()
__settings__ = Settings.Settings(GuiLogger.guiLogger)
__session__ = Adapter.Adapter(__settings__)

gui = Gui.Gui(__session__)
gui.display()
