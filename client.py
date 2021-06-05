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
            print("execute: invite: " + command[1]) 
            sipSession.invite(command[1])
            
        if command[0] == 'exit' or command[0] == 'quit':
            os._exit(1)
