from datetime import datetime
import logging
import time
import sip.Session
import sip.Client
import sip.Network
import os

logging.basicConfig(filename="sipclient.log", level=logging.INFO)
logging.getLogger(__name__)

if __name__ == "__main__":
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    logging.info("\r\nSIP Client starts at: " + str(timestamp) + '\r\n')

    sipClient = None
    sipSession = None
    receiver = None

    while True:
        command = str(input("Waiting for command...\n"))
        command = command.split()
        print(command)

        if command[0] == 'register':
            print('execute: register')
            sipClient = sip.Client.Client()
            sipSession = sip.Session.Session(sipClient)
            receiver = sip.Network.Receiver(sipClient.network, sipSession, 1)
            sipSession.register()

        if command[0] == 'invite':
            idUser = '103'
            print("execute: invite: ", idUser) 
            sipSession.invite(idUser)
            
        if command[0] == '-h':
            print("register invite exit")
        
        if command[0] == 'exit' or command[0] == 'quit':
            os._exit(1)

# ffmpeg
# From Bardowski Pawel to Everyone:  01:47 PM
#  ffmpeg.exe -i Runner-1080p\\libx265\\6750\\encoded.mp4 -vb 6750k -maxrate 6750k -bufsize 6750k -filter:v fps=30000/1001 -vcodec libx265 -preset medium -x265-params keyint=10:min-keyint=10 -sdp_file Runner-1080p\\libx265\\6750\\rtp\\.info.sdp -strict 2 -f rtp rtp://127.0.0.1:16500

# ffmpeg -re -i sample.mp3 -vn -f mulaw -f rtp rtp://127.0.0.1:51372
# INVITE do nas, CANCEL, BYE od nas
