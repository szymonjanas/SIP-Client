import threading
import sip.messages
import sip.serialize
import sip.authorization
import sip.Client
import sip.header
import logging

__logger__ = logging.getLogger(__name__)

class Session(threading.Thread):
    def __init__(self, p_client):
        self.client = p_client
        self.last_response = None
        self.callID = sip.header.callID()
        self.senderQ = list()

        threading.Thread.__init__(self)
        self.deamon = True
        self.start()

    def run(self):
        print()

    def register(self):
        registerMsg = sip.messages.REGISTER(p_client=self.client, p_callID=self.callID)
        self.client.network.send(   registerMsg,
                                    self.client.config.domain,
                                    self.client.config.sipPORT)

    def invite(self, p_usernameDest='100'):
        inviteMsg = sip.messages.INVITE(p_client = self.client, 
                                        p_username_dest=p_usernameDest,
                                        p_callID = self.callID)
        self.senderQ.append(inviteMsg)

    

    def process(self, p_response : sip.Network.Response):
        t_response = sip.serialize.decodeRequest(p_response.data)
        self.last_response = t_response
        if t_response["Message"] == 'SIP/2.0 401 Unauthorized':
            registerWithAuth = sip.messages.REGISTER(
                                    p_client = self.client, p_callID = self.callID,
                                    p_authorization=sip.authorization.Authorization(p_nonce=t_response['nonce'],
                                                                                    p_realm=t_response['realm'],
                                                                                    p_method=t_response['method']))
            self.client.network.send(   registerWithAuth,
                                        self.client.config.domain,
                                        self.client.config.sipPORT)
            return

        if t_response["Message"] == 'SIP/2.0 200 OK':
            self.client.isRegister = True
            print("200 OK")
            __logger__.info("200 OK")
 
        if t_response["Message"] == 'SIP/2.0 100 Trying':
            print("Trying...")
            __logger__.info("Trying...")

        while not bool(len(self.senderQ)):
            pass

        itemToSend = self.senderQ.pop(0)
        self.client.network.send(   itemToSend, 
                                    self.client.config.domain,
                                    self.client.config.sipPORT)

