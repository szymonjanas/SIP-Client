import threading
import sip.requests
import sip.responses
import sip.serialize
import sip.authorization
import sip.Client
import sip.header
import sip.Audio
import logging
import time
import copy

__logger__ = logging.getLogger(__name__)

class STATE:
    IDLE = 0
    REGISTER = 1
    INVITE = 2
    CONNECTED = 3
    BYE = 4

class Session(threading.Thread):
    def __init__(self, p_client):
        self.client = p_client
        self.last_response = None
        self.callID = sip.header.callID()

        self.audio = sip.Audio.Audio()

        threading.Thread.__init__(self)
        self.deamon = True

        self.username_destination = '100'
        self.STATE = STATE.IDLE
        self.expires = 120
        self.lastRegister = 0
        self.isRegister = False
        self.reregister = True

        self.callDetails = sip.header.CallDetails()

        self.start()

    def __del__(self):
        self.reregister = False
        self.audio.stop()

    def run(self):
        while self.reregister:
            if self.isRegister:
                if time.time() - self.lastRegister >= self.expires - int(0.1*self.expires):
                    self.register()

    def getState(self):
        return self.STATE

    def register(self, p_auth=None):
        self.STATE = STATE.REGISTER
        self.lastRegister = time.time()
        registerMsg = None
        if p_auth == None:
            registerMsg = sip.requests.REGISTER(p_client=self.client, p_callDetails=self.callDetails)
        else:
            registerMsg = sip.requests.REGISTER(p_client=self.client, 
                                                p_callDetails=self.callDetails,
                                                p_authorization=p_auth)
        self.client.network.send(   registerMsg,
                                    self.client.config.domain,
                                    self.client.config.sipPORT)

    def invite(self, p_usernameDest=None):
        self.STATE = STATE.INVITE
        if p_usernameDest == None:
            p_usernameDest = self.username_destination
        else:
            self.username_destination = p_usernameDest
        inviteMsg = sip.requests.INVITE(p_client = self.client, 
                                        p_username_dest=p_usernameDest,
                                        p_callDetails=self.callDetails,
                                        p_contentSDP = self.audio.getSdpSipMessage())
        self.client.network.send(   inviteMsg,
                                    self.client.config.domain,
                                    self.client.config.sipPORT)

    def ack(self):
        if self.STATE == STATE.INVITE:
            self.STATE = STATE.CONNECTED
        ackMsg = sip.requests.ACK(  p_client = self.client,
                                    p_username_dest = self.username_destination,
                                    p_callDetails=self.callDetails)
        self.client.network.send(   ackMsg,
                                    self.client.config.domain,
                                    self.client.config.sipPORT)
    def cancel(self):
        if self.STATE == STATE.INVITE:
            self.STATE = STATE.IDLE
            cancelMsg = sip.requests.CANCEL( p_client = self.client,
                                            p_username_dest = self.username_destination,
                                            p_callDetails=self.callDetails)
            self.client.network.send(   cancelMsg,
                                        self.client.config.domain,
                                        self.client.config.sipPORT)
        elif self.STATE == STATE.CONNECTED:
            self.bye()

    def bye(self):
        if self.STATE == STATE.CONNECTED:
            self.STATE = STATE.IDLE
            byeMsg = sip.requests.BYE(  p_client = self.client,
                                        p_username_dest = self.username_destination,
                                        p_callDetails=self.callDetails)
            self.client.network.send(   byeMsg,
                                        self.client.config.domain,
                                        self.client.config.sipPORT)

    def stop(self):
        self.audio.stop()
        self.STATE = STATE.IDLE

    def r_ok(self, p_requestResponse, p_cseq, p_tag, p_contactPort):
        t_callDetails = copy.deepcopy(self.callDetails)
        t_callDetails.cseq = p_cseq
        okRespMsg = sip.responses.RESPONSE( sip.responses.RESPONSES.OK200,
                                            p_username=self.client.config.username,
                                            p_username_dest=self.username_destination,
                                            p_domain=self.client.config.domain,
                                            p_clientIP=self.client.config.domain,
                                            p_clientPORT=self.client.config.sipPORT,
                                            p_userAgent=self.client.config.userAgent,
                                            p_callDetails=t_callDetails,
                                            p_contactPort=p_contactPort,
                                            p_tagFrom=p_tag,
                                            p_requestResponse=p_requestResponse)
        self.client.network.send(   okRespMsg,
                                    self.client.config.domain, 
                                    self.client.config.sipPORT)

    def process(self, p_response : sip.Network.Response):
        t_response = sip.serialize.decodeRequest(p_response.data)
        self.last_response = t_response

        if t_response["Message"] == 'SIP/2.0 401 Unauthorized':
            self.client.log('Unauthorized.')
            authDetails = sip.authorization.Authorization( p_nonce=t_response['nonce'],
                                                                    p_realm=t_response['realm'],
                                                                    p_method=t_response['method'])
            self.register(authDetails)

        elif t_response["Message"] == 'SIP/2.0 200 OK':
            if self.STATE == STATE.REGISTER:
                log = '200 OK. Registered!'
                self.expires = int(t_response['expires'])
                self.isRegister = True
                self.client.log(log)
                __logger__.info(log)
            elif self.STATE == STATE.INVITE:
                log = '200 OK. Call in progress...'
                self.client.log(log)
                __logger__.info(log)
                self.ack()
                try:
                    self.audio.play(t_response['audio-port'])
                except KeyError as kr:
                    __logger__.warning(kr)
                    self.audio.play()
            elif self.STATE == STATE.IDLE:
                self.client.log('200 OK. Canceled!')
 
        elif t_response["Message"] == 'SIP/2.0 100 Trying':
            self.client.log('Trying...')
            __logger__.info("Trying...")

        elif t_response["Message"] == 'SIP/2.0 180 Ringing':
            self.client.log('Ringing...')
            __logger__.info("Ringing...")

        elif t_response["Message"] == 'SIP/2.0 480 Temporarily Unavailable':
            self.client.log('Temporarily Unavailable.')
            __logger__.info("Temporarily Unavailable.")
            self.ack()
        
        elif t_response["Message"].split()[0] == 'BYE':
            self.client.log('Bye...')
            __logger__.info("Bye...")
            self.audio.stop()
            self.r_ok(p_requestResponse='BYE', p_cseq=t_response['cseq'], p_tag=t_response['tag'], p_contactPort=t_response['contactPort'])

        elif t_response["Message"] == 'SIP/2.0 487 Request Terminated':
            self.client.log('Request Terminated!')
            __logger__.info("Request Terminated!")
            self.ack()
