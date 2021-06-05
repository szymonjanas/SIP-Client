import sip.Network

class Config:
    def __init__(   self,
                    p_clientPORT : int,
                    p_username : str,
                    p_domain : str,
                    p_clientIP : str,
                    p_expires : int,
                    p_sipPORT : int,
                    p_password : str,
                    p_userAgent : str):
        self.username = p_username
        self.domain = p_domain
        self.clientIP = p_clientIP
        self.clientPORT = p_clientPORT
        self.expires=p_expires
        self.sipPORT=p_sipPORT
        self.password=p_password
        self.userAgent = p_userAgent

class Client:
    def __init__(   self,
                    p_username : str ="101",
                    p_domain : str ="127.0.0.1",
                    p_clientIP : str ='127.0.0.1',
                    p_network : sip.Network.NetworkConnector = None,
                    p_expires : int  =120,
                    p_sipPORT : int =5060,
                    p_password : str ='101',
                    p_userAgent : str = 'BAJS-phone'):
        self.network = p_network
        if self.network is None:
            self.network = sip.Network.NetworkConnector(p_domain)
        self.config = Config(
            p_username = p_username,
            p_domain = p_domain,
            p_clientIP = p_clientIP,
            p_clientPORT = self.network.getPort(),
            p_expires=p_expires,
            p_sipPORT=p_sipPORT,
            p_password=p_password,
            p_userAgent=p_userAgent)
        self.isRegister = False
        self.history = list()
