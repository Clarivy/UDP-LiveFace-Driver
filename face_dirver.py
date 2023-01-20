from facedriver.BS_parser import BS_Parser
from facedriver.timecode import Timecode
from facedriver.UDP_utils import UDP_Sender
import time
import threading

class FaceDriver():

    def __init__(self, bs_parser: BS_Parser = None, udp_sender: UDP_Sender = None):
        self._bs_parser = bs_parser
        self._udp_sender = udp_sender
        if self._bs_parser is None:
            self._bs_parser = BS_Parser()
        if self._udp_sender is None:
            self._udp_sender = UDP_Sender(IP="localhost", port=11111)
        
    def send(self, bs_path: str):
        self._bs_parser.parse_npy(bs_path)
        print("Sending...")
        for frame in self._bs_parser:
            self._udp_sender.send(frame)
            time.sleep(0.01)
        print("sent.")
        self._bs_parser.clear_buffer()