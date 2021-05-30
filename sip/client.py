import sip.session
import sip.messages
import sip.serialize
import sip.authorization

class Client:
    def __init__(self):
        self.session = sip.session.Session("192.168.56.1")
        self.session.send(sip.messages.REGISTER(p_username="101", 
                                     p_domain="127.0.0.1",
                                     p_clientIP="192.168.56.1",
                                     p_clientPORT="55610",
                                     p_expires=3600,
                                     p_tag="dd022aced4fbd05a"),
                            "127.0.0.1",
                            5060)
        self.counter = 0
        self.receiver(self.session.recv())

    def receiver(self, p_data):
        t_data = sip.serialize.decodeRequest(p_data.data)
        if t_data["Message"] == 'SIP/2.0 401 Unauthorized':
            self.session.send(sip.messages.REGISTER(p_username="101", 
                                    p_domain="127.0.0.1",
                                    p_clientIP="192.168.56.1",
                                    p_clientPORT="55610",
                                    p_expires=3600,
                                    p_tag="dd022aced4fbd05a",
                                    p_password="101",
                                    p_authorization=sip.authorization.Authorization(p_nonce=t_data['nonce'],
                                                                                    p_realm=t_data['realm'],
                                                                                    p_method=t_data['method'])),
                        "127.0.0.1",
                        5060)
            self.counter += 1
            if not self.counter > 2:
                self.receiver(self.session.recv())

