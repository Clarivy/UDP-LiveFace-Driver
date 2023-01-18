from BS_parser import BS_Parser, USC55_to_ARKIT_Wrapper, DataFrameWrapper
from timecode import Timecode
from UDP_utils import UDP_Reciever, UDP_Sender
import time

timecode = Timecode(start_frame_num=4329111,start_subframe=0.1,FRAME_RATE_DEN=30)

# bs_parser = BS_Parser(timecode=Timecode(start_frame_num=40,start_subframe=0.1,FRAME_RATE_DEN=60), dataframe_wrapper=DataFrameWrapper())
# npy_file = "./csv.npy"


bs_parser = BS_Parser(timecode=timecode, dataframe_wrapper=USC55_to_ARKIT_Wrapper())
npy_file = "./test_xi.npy"
# npy_file = "./BS.npy"

result_file = './result.bin'

bs_parser.parse_npy(npy_filename=npy_file)
# bs_parser.parse_npy(npy_filename=npy_file)
# bs_parser.parse_npy(npy_filename=npy_file)
# bs_parser.parse_npy(npy_filename=npy_file)
# bs_parser.parse_npy(npy_filename=npy_file)
# bs_parser.parse_npy(npy_filename=npy_file)

sender = UDP_Sender(IP="localhost", port=11111)

f = open(result_file, 'wb')

for package in bs_parser:
    sender.send(package)
    time.sleep(1/30)
    f.write(package)

f.close()

