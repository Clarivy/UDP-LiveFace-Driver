import struct
import typing

class Timecode():

    def __init__(self,
        start_frame_num: int = 0,
        start_subframe: float = 0.,
        FRAME_RATE_NUM: int = 1,
        FRAME_RATE_DEN: int = 30,
        byteorder: typing.Literal['big', 'little'] = 'big'
    ) -> None:

        self.current_frame_num = start_frame_num
        self.current_subframe = start_subframe
        self.FRAME_RATE_NUM = FRAME_RATE_NUM
        self.FRAME_RATE_DEN = FRAME_RATE_DEN
        self.set_byteorder(byteorder=byteorder)
    
    def set_byteorder(self, byteorder: typing.Literal['big', 'little']) -> None:
        self.byteorder = byteorder
        self.timecode_format = ">" if self.byteorder == 'big' else "<"
        self.timecode_format = self.timecode_format + "ifii"
    
    def get_frame_interval(self) -> float:
        return self.FRAME_RATE_DEN / self.FRAME_RATE_NUM

    def get_timecode_bytes(self) -> bytes:
        """
        Returns the current timecode as a 16-byte string

        Format:
        0-3: frame number: int32
        4-7: subframe number: float32
        8-11: frame rate numerator: int32
        12-15: frame rate denominator: int32

        """

        return struct.pack(
            self.timecode_format,
            self.current_frame_num,
            self.current_subframe,
            self.FRAME_RATE_DEN,
            self.FRAME_RATE_NUM,
        )
    
    def __next__(self) -> bytes:
        self.current_frame_num += 1

        return self.get_timecode_bytes()

    def __iter__(self):
        return self