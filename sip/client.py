import sip.session
import sip.messages
import sip.serialize
import sip.authorization

class Client:
    def __init__(self):
        self.username=str("101")
        self.domain="127.0.0.1"
        self.clientIP='127.0.0.1'
        self.session = sip.session.Session('127.0.0.1')
        self.clientPORT=self.session.getPort()
        self.expires=3600
        self.tag="dd022aced4fbd05a"
        self.sipPORT=5060
        self.password='101'

        self.last_response = None

        self.session.bind()

        self.register()
        self.invite()


    def register(self):
        self.session.send(sip.messages.REGISTER(p_username=self.username, 
                                     p_domain=self.domain,
                                     p_clientIP=self.clientIP,
                                     p_clientPORT=self.clientPORT,
                                     p_expires=self.expires,
                                     p_tag="dd022aced4fbd05a"),
                            self.domain,
                            self.sipPORT)
        self.counter = 0
        self.receiver(self.session.recv())

    def invite(self, ):
        self.session.send(sip.messages.INVITE(p_username=self.username, 
                                        p_username_dest="100",
                                        p_domain=self.domain,
                                        p_clientIP=self.clientIP,
                                        p_clientPORT=str(self.clientPORT),
                                        p_tag="dd022aced4fbd05a",
                                        p_callID=self.last_response['call-id']),
                                self.domain,
                                self.sipPORT)
        self.counter = 0
        self.receiver(self.session.recv())

    def receiver(self, p_data):
        t_data = sip.serialize.decodeRequest(p_data.data)
        self.last_response = t_data
        if t_data["Message"] == 'SIP/2.0 401 Unauthorized':
            self.session.send(sip.messages.REGISTER(p_username=self.username, 
                                     p_domain=self.domain,
                                     p_clientIP=self.clientIP,
                                     p_clientPORT=self.clientPORT,
                                     p_expires=self.expires,
                                    p_password=self.password,
                                    p_tag="dd022aced4fbd05a",
                                    p_authorization=sip.authorization.Authorization(p_nonce=t_data['nonce'],
                                                                                    p_realm=t_data['realm'],
                                                                                    p_method=t_data['method'])),
                        self.domain,
                        self.sipPORT)
            self.counter += 1
            if not self.counter > 2:
                self.receiver(self.session.recv())

