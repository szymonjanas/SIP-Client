import socket
import logging
import threading
import sip.messages
import sip.helpers

__logger__ = logging.getLogger(__name__)
__logger__.setLevel(10)

class Response:
    def __init__(self, p_data, p_addr):
        self.data = p_data
        self.addr = p_addr

class NetworkConnector:
    def __init__(self,
                 p_clientIP : str = "127.0.0.1"):
        self.clientIP = p_clientIP
        self.bind_port = None
        self.sipSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.bind()

    def bind(self):
        self.sipSocket.bind(("127.0.0.1", 0))
        self.bind_port = self.sipSocket.getsockname()[1]
        __logger__.warning("sipSocket bind with addr: " + self.clientIP + ":" + str(self.bind_port))

    def getPort(self):
        if self.bind_port == None:
            __logger__.error("Session not binded!")
        return self.bind_port

    def send(self, message : str, ip : str, port : int):
        self.sipSocket.sendto(sip.helpers.encode(message), (ip, port))
        __logger__.info("SEND: " + message)

    def recv(self):
        data, addr = self.sipSocket.recvfrom(2048)
        __logger__.info("RECV FROM: " + str(addr) + "; MESSAGE: " + str(data) + '\r\n')
        return Response(sip.helpers.decode(data), addr)

class Receiver(threading.Thread):
    def __init__(self, p_networkConnector : NetworkConnector, p_callback, i):
        self.networkConnector = p_networkConnector
        self.callback = p_callback
        threading.Thread.__init__(self)
        self.deamon = True
        self.h = i
        self.status = True
        self.start()

    def run(self):
        try:
            while self.status:
                self.callback.process(self.networkConnector.recv())
        except Exception as ex:
            print(ex.what())
