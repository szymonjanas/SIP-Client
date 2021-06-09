import threading
import sip.messages
import sip.serialize
import sip.authorization
import sip.Client
import sip.header
import sip.Audio
import logging

__logger__ = logging.getLogger(__name__)

class Session(threading.Thread):
    def __init__(self, p_client):
        self.client = p_client
        self.last_response = None
        self.callID = sip.header.callID()
        self.senderQ = list()

        self.audio = sip.Audio.Audio()

        threading.Thread.__init__(self)
        self.deamon = True
        self.start()

        self.username_destination = '100'
        self.STATE = 'Idle'

    def run(self):
        print()

    def register(self):
        self.STATE = 'Register'
        registerMsg = sip.messages.REGISTER(p_client=self.client, p_callID=self.callID)
        self.client.network.send(   registerMsg,
                                    self.client.config.domain,
                                    self.client.config.sipPORT)

    def invite(self, p_usernameDest=None):
        self.STATE = 'Invite'
        if p_usernameDest == None:
            p_usernameDest = self.username_destination
        else:
            self.username_destination = p_usernameDest
        inviteMsg = sip.messages.INVITE(p_client = self.client, 
                                        p_username_dest=p_usernameDest,
                                        p_callID = self.callID,
                                        p_contentSDP = self.audio.getSdpSipMessage())
        self.client.network.send(   inviteMsg,
                                    self.client.config.domain,
                                    self.client.config.sipPORT)

    def ack(self):
        ackMsg = sip.messages.ACK(  p_client = self.client,
                                    p_username_dest = self.username_destination,
                                    p_callID = self.callID)
        self.client.network.send(   ackMsg,
                                    self.client.config.domain,
                                    self.client.config.sipPORT)

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
            if self.STATE == 'Register':
                self.client.isRegister = True
                print("200 OK")
                __logger__.info("200 OK")
            elif self.STATE == 'Invite':
                print("200 OK")
                __logger__.info("200 OK")
                self.ack()
                try:
                    self.audio.play(t_response['audio-port'])
                except KeyError as kr:
                    __logger__.warning(kr)
                    self.audio.play()
 
        if t_response["Message"] == 'SIP/2.0 100 Trying':
            print("Trying...")
            __logger__.info("Trying...")

        if t_response["Message"] == 'SIP/2.0 180 Ringing':
            print("Ringing...")
            __logger__.info("Ringing...")

        if t_response["Message"] == 'SIP/2.0 480 Temporarily Unavailable':
            print("Temporarily Unavailable...")
            __logger__.info("Temporarily Unavailable...")
            self.ack()
        
        if t_response["Message"].split()[0] == 'BYE':
            self.STATE = "Bye"
            print("Bye...")
            __logger__.info("Bye...")
            self.audio.stop()
