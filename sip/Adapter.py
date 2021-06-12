from sip import Session, Client, Network
import settings.Settings

class Adapter:
    def __init__(self, p_settings : settings.Settings.Settings):
        self.settings = p_settings
        self.session = None
        self.receiver = None

        self.__loadClient__()

    def callTo(self, number):
        self.session.invite(number)

    def cancel(self):
        self.session.cancel()
        self.session.stop()

    def getSettings(self):
        sett = self.settings.load()
        self.__loadClient__(sett)
        return sett

    def getState(self):
        return self.session.getState()

    def setSettings(self, p_username, p_password, p_addressIp):
        self.settings.save(p_username, p_password, p_addressIp)
        self.__loadClient__()

    def __loadClient__(self, sett = None):
        if sett == None:
            sett = self.settings.load()
        try:
            self.client = Client.Client(p_username=sett.username,
                                        p_password=sett.password,
                                        p_domain=sett.addressIp)
            self.session = Session.Session(self.client)
            self.receiver = Network.Receiver(self.client.network, self.session, 1)
            self.session.register()
            self.client.setGuiLogger(self.settings.guiLogger)
            self.settings.guiLogger.log('Client registered to server!')
        except ConnectionResetError as cre:
            self.settings.guiLogger.log("Client can not connect to sip server: " + str(cre))

    def __del__(self):
        if self.session != None:
            self.session.__del__()
        if self.receiver != None:
            self.receiver.__del__()
