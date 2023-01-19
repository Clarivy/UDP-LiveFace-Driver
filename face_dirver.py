from BS_parser import BS_Parser
from timecode import Timecode
from UDP_utils import UDP_Sender
import time
import threading

class FaceDriver():

    def __init__(self, timecode: Timecode = None, bs_parser: BS_Parser = None, udp_sender: UDP_Sender = None):
        self._timecode = timecode
        self._bs_parser = bs_parser
        self._udp_sender = udp_sender
        if self._timecode is None:
            self._timecode = Timecode(start_frame_num=0, start_subframe=0.1, FRAME_RATE_DEN=30)
        if self._bs_parser is None:
            self._bs_parser = BS_Parser(timecode=self._timecode)
        if self._udp_sender is None:
            self._udp_sender = UDP_Sender(IP="localhost", port=11111)
        
    def send(self, bs_path: str):
        self._bs_parser.parse_npy(bs_path)
        for frame in self._bs_parser.frames:
            self._udp_sender.send(frame)
            time.sleep(self._timecode.get_frame_interval())
        self._bs_parser.clear_buffer()