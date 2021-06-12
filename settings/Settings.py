import json
import logging 

__logger__ = logging.getLogger(__name__)

class SettingsItem:
    def __init__(self, p_username, p_password, p_addressIp):
        self.username = p_username
        self.password = p_password
        self.addressIp = p_addressIp
    
    def toJson(self):
        data = dict()
        data['username'] = self.username
        data['password'] = self.password
        data['addressIp'] = self.addressIp
        return data

class Settings:
    def __init__(self, p_guiLogger, p_path='settings.json'):
        self.path = p_path
        self.object = None
        self.guiLogger = p_guiLogger
        self.counter = 0
        
    def load(self):
        try:
            log = 'Load setting from file: ' + self.path
            __logger__.warning(log)
            self.guiLogger.log(log)
            self.file = open(self.path, 'r')
            jobject = json.load(self.file)
            self.object = SettingsItem(jobject['username'], jobject['password'], jobject['addressIp'])
            self.guiLogger.log('Loaded.')
        except Exception as ex:
            log = "Problem with reading json settings file: " + self.path + ", exception: " + str(ex)
            self.guiLogger.log(log)
            __logger__.error(log)
            return 
        return self.object

    def save(self, p_username, p_password, p_address):
        try:
            p_settingsItem = SettingsItem(p_username, p_password, p_address)
            log = 'Save setting to file: ' + self.path
            self.guiLogger.log(log)
            self.object = p_settingsItem
            self.file = open(self.path, 'w')
            json.dump(self.object.toJson(), self.file)
            self.guiLogger.log('Saved.')
        except Exception as ex:
            __logger__.error('Exception occured! ' + str(ex))
            self.guiLogger.log(log)
            
    def get(self):
        if self.object == None:
            __logger__.warning("File not loaded! Load json settings file to get settings!")
            return SettingsItem('','','')
        return self.object
