import subprocess
import logging

__logger__ = logging.getLogger(__name__)

class Audio:
    def __init__(self):
        self.playing = None
        self.port = 20002
        self.ip = '192.168.1.103'

    def getSdpSipMessage(self):
        sdpOut = str()
        sdpOut += 'v=0\r\n'
        sdpOut += 'o=- 0 0 IN IP4 {}\r\n'.format('127.0.0.1')
        sdpOut += 's=No Name\r\n'
        sdpOut += 'c=IN IP4 {}\r\n'.format(self.ip)
        sdpOut += 't=0 0\r\n'
        sdpOut += 'a=tool:libavformat 58.76.100\r\n'
        sdpOut += 'm=audio {} RTP/AVP 0\r\n'.format(self.port)
        sdpOut += 'b=AS:64\r\n'
        return sdpOut

    def play(self, p_port=None):
        if p_port == None:
            p_port = self.port
        path = 'E:\\PWr\\Semestr6\\UiSMUrządzeniaISystemyMultimedialne\\ProjektSIP\\Program\\SIP-Client\\'
        cmd = 'ffmpeg.exe -re -i {path}sample_u-law.wav -vn -f mulaw -f rtp rtp://{ip}:{port}'.format(path=path, ip=self.ip, port=p_port)
        __logger__.info("Audio execute: " + cmd)
        # self.playing = subprocess.Popen(cmd.split())

    def stop(self):
        if self.playing != None:
            self.playing.terminate()
            self.playing.wait()
            __logger__.info("Audio stoped!")

    def __del__(self):
        self.stop()
