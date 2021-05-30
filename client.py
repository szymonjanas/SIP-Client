import sip.client
import sip.session
import logging

logging.basicConfig(filename="sipclient.log", level=logging.INFO)
logging.getLogger(__name__)
logging.info("hello")
sipClient = sip.client.Client()
