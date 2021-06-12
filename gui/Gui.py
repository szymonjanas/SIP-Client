from typing import Set
from PyQt5.QtWidgets import *
from PyQt5 import uic
import time, os

MainForm, _ = uic.loadUiType("gui/ui/main.ui")
SettingsForm, _ = uic.loadUiType("gui/ui/settings.ui")

class SettingsWindow(QDialog, SettingsForm):
    def __init__(self, p_session, p_applicationName):
        super(SettingsWindow, self).__init__()
        self.session = p_session
        self.setupUi(self)
        self.labelApplicationName.setText(p_applicationName)

        self.btnSave.clicked.connect(self.onClick_btnSave)
        self.btnCancel.clicked.connect(self.onClick_btnCancel)

    def open(self):
        sett = self.session.getSettings()
        self.setInput_inputUsername(sett.username)
        self.setInput_inputPassword(sett.password)
        self.setInput_inputAddressIp(sett.addressIp)
        self.show()

    def onClick_btnSave(self):
        un = self.getInput_inputUsername()
        pas = self.getInput_inputPassword()
        addr = self.getInput_inputAddressIp()
        self.session.settings.save(un, pas, addr)

    def onClick_btnCancel(self):
        self.close()

    def getInput_inputUsername(self):
        return self.inputUsername.text()

    def getInput_inputPassword(self):
        return self.inputPassword.text()

    def getInput_inputAddressIp(self):
        return self.inputAddressIp.text()

    def setInput_inputUsername(self, username):
        self.inputUsername.setText(username)

    def setInput_inputPassword(self, password):
        self.inputPassword.setText(password)

    def setInput_inputAddressIp(self, addressIp):
        self.inputAddressIp.setText(addressIp)

class MainWindow(QDialog, MainForm):
    def __init__(self, p_session, p_applicationName = 'simple SIP phone'):
        super(MainWindow, self).__init__()
        self.settingsWindow = SettingsWindow(p_session, p_applicationName)
        self.session = p_session
        self.session.settings.guiLogger.init(self.logBoxAppend)
        self.setupUi(self)

        self.labelApplicationName.setText(p_applicationName)
        self.logBox.setReadOnly(True)
        
        self.btnCall.clicked.connect(self.onClick_btnCall)
        self.btnStop.clicked.connect(self.onClick_btnStop)
        self.btnSettings.clicked.connect(self.onClick_btnSettings)
        self.btnCleanLogBox.clicked.connect(self.onClick_btnCleanLogBox)

        self.cleanAll = time.time()
        
    def onClick_btnCall(self):
        number = str(self.getInputNumber())
        self.session.callTo(number)
        if self.session.getState() == 'Invite':
            self.btnStop.setText('Zakończ')

    def onClick_btnStop(self):
        if self.session.getState() == 'Register':
            self.inputNumber.setText('')
        elif self.session.getState() == 'Invite':
            self.session.cancel()
            self.btnStop.setText('Anuluj')

    def onClick_btnSettings(self):
        self.settingsWindow.open()

    def onClick_btnCleanLogBox(self):
        self.logBoxClean()
        if  time.time() - self.cleanAll < 1:
            self.inputNumber.setText('')
        self.cleanAll = time.time()
    
    def getInputNumber(self):
        return self.inputNumber.text()

    def logBoxAppend(self, message):
        self.logBox.append(message)

    def logBoxClean(self):
        self.logBox.setText('')

class Gui:
    def __init__(self, p_session):
        self.app = QApplication([])
        self.session = p_session
        self.mainWindow = MainWindow(p_session)
        self.app.aboutToQuit.connect(self.myExitHandler)

    def display(self):
        self.mainWindow.show()
        self.app.exec_()

    def myExitHandler(self):
        self.session.__del__()
        os._exit(1)
