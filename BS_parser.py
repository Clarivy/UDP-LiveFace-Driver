import numpy as np
from timecode import Timecode

NAMES_ARKIT = ['EyeBlinkLeft', 'EyeLookDownLeft', 'EyeLookInLeft', 'EyeLookOutLeft', 'EyeLookUpLeft', 'EyeSquintLeft', 'EyeWideLeft', 'EyeBlinkRight', 'EyeLookDownRight', 'EyeLookInRight', 'EyeLookOutRight', 'EyeLookUpRight', 'EyeSquintRight', 'EyeWideRight', 'JawForward', 'JawRight', 'JawLeft', 'JawOpen', 'MouthClose', 'MouthFunnel', 'MouthPucker', 'MouthRight', 'MouthLeft', 'MouthSmileLeft', 'MouthSmileRight', 'MouthFrownLeft', 'MouthFrownRight', 'MouthDimpleLeft', 'MouthDimpleRight', 'MouthStretchLeft', 'MouthStretchRight', 'MouthRollLower', 'MouthRollUpper', 'MouthShrugLower', 'MouthShrugUpper', 'MouthPressLeft', 'MouthPressRight', 'MouthLowerDownLeft', 'MouthLowerDownRight', 'MouthUpperUpLeft', 'MouthUpperUpRight', 'BrowDownLeft', 'BrowDownRight', 'BrowInnerUp', 'BrowOuterUpLeft', 'BrowOuterUpRight', 'CheekPuff', 'CheekSquintLeft', 'CheekSquintRight', 'NoseSneerLeft', 'NoseSneerRight', 'TongueOut', 'HeadYaw', 'HeadPitch', 'HeadRoll', 'LeftEyeYaw', 'LeftEyePitch', 'LeftEyeRoll', 'RightEyeYaw', 'RightEyePitch', 'RightEyeRoll']
NAMES_USC55 = ["browDown_L", "browDown_R", "browInnerUp_L", "browInnerUp_R", "browOuterUp_L", "browOuterUp_R", "cheekPuff_L", "cheekPuff_R", "cheekRaiser_L", "cheekRaiser_R", "cheekSquint_L", "cheekSquint_R", "eyeBlink_L", "eyeBlink_R", "eyeLookDown_L", "eyeLookDown_R", "eyeLookIn_L", "eyeLookIn_R", "eyeLookOut_L", "eyeLookOut_R", "eyeLookUp_L", "eyeLookUp_R", "eyeSquint_L", "eyeSquint_R", "eyeWide_L", "eyeWide_R", "jawForward", "jawLeft", "jawOpen", "jawRight", "mouthClose", "mouthDimple_L", "mouthDimple_R", "mouthFrown_L", "mouthFrown_R", "mouthFunnel", "mouthLeft", "mouthLowerDown_L", "mouthLowerDown_R", "mouthPress_L", "mouthPress_R", "mouthPucker", "mouthRight", "mouthRollLower", "mouthRollUpper", "mouthShrugLower", "mouthShrugUpper", "mouthSmile_L", "mouthSmile_R", "mouthStretch_L", "mouthStretch_R", "mouthUpperUp_L", "mouthUpperUp_R", "noseSneer_L", "noseSneer_R"]
NAMES_USC55_from_ARKIT = { "browDown_L": "BrowDownLeft", "browDown_R": "BrowDownRight", "browInnerUp_L": "BrowInnerUp", "browInnerUp_R": "BrowInnerUp", "browOuterUp_L": "BrowOuterUpLeft", "browOuterUp_R": "BrowOuterUpRight", "cheekPuff_L": "CheekPuff", "cheekPuff_R": "CheekPuff", "cheekRaiser_L": "", "cheekRaiser_R": "", "cheekSquint_L": "CheekSquintLeft", "cheekSquint_R": "CheekSquintRight", "eyeBlink_L": "EyeBlinkLeft", "eyeBlink_R": "EyeBlinkRight", "eyeLookDown_L": "EyeLookDownLeft", "eyeLookDown_R": "EyeLookDownRight", "eyeLookIn_L": "EyeLookInLeft", "eyeLookIn_R": "EyeLookInRight", "eyeLookOut_L": "EyeLookOutLeft", "eyeLookOut_R": "EyeLookOutRight", "eyeLookUp_L": "EyeLookUpLeft", "eyeLookUp_R": "EyeLookUpRight", "eyeSquint_L": "EyeSquintLeft", "eyeSquint_R": "EyeSquintRight", "eyeWide_L": "EyeWideLeft", "eyeWide_R": "EyeWideRight", "jawForward": "JawForward", "jawLeft": "JawLeft", "jawOpen": "JawOpen", "jawRight": "JawRight", "mouthClose": "MouthClose", "mouthDimple_L": "MouthDimpleLeft", "mouthDimple_R": "MouthDimpleRight", "mouthFrown_L": "MouthFrownLeft", "mouthFrown_R": "MouthFrownRight", "mouthFunnel": "MouthFunnel", "mouthLeft": "MouthLeft", "mouthLowerDown_L": "MouthLowerDownLeft", "mouthLowerDown_R": "MouthLowerDownRight", "mouthPress_L": "MouthPressLeft", "mouthPress_R": "MouthPressRight", "mouthPucker": "MouthPucker", "mouthRight": "MouthRight", "mouthRollLower": "MouthRollLower", "mouthRollUpper": "MouthRollUpper", "mouthShrugLower": "MouthShrugLower", "mouthShrugUpper": "MouthShrugUpper", "mouthSmile_L": "MouthSmileLeft", "mouthSmile_R": "MouthSmileRight", "mouthStretch_L": "MouthStretchLeft", "mouthStretch_R": "MouthStretchRight", "mouthUpperUp_L": "MouthUpperUpLeft", "mouthUpperUp_R": "MouthUpperUpRight", "noseSneer_L": "NoseSneerLeft", "noseSneer_R": "NoseSneerRight", }

class DataFrameWrapper():
    
    def __init__(self,
        byteorder: str = 'big',
    ) -> None:
        self._byteorder = byteorder
        self.float_format = (">" if self._byteorder == 'big' else "<") + "f4"

    def parse(self, data: np.ndarray) -> None:
        package = bytearray()
        BS_NUM = len(data)
        print("Send data", data[-5:])
        # data[-9:] *= 0
        BS_NUM_BYTES = BS_NUM.to_bytes(1, byteorder=self._byteorder)
        package.extend(BS_NUM_BYTES)
        package.extend(data.astype(self.float_format).tobytes('C'))
        return package
        
    def set_byteorder(self, byteorder: str) -> None:
        self._byteorder = byteorder

class ExtendDataFrameWrapper(DataFrameWrapper):
    
    def __init__(self,
        data_len,
        byteorder: str = 'big'
    ) -> None:
        super().__init__(byteorder=byteorder)
        self._data_len = data_len
    
    def parse(self, data: np.ndarray) -> bytearray:
        if len(data) < self._data_len:
            data = np.pad(data, (0, self._data_len - len(data)), 'constant', constant_values=(0., 0.))
        if len(data) > self._data_len:
            raise Exception("Data is too long for this package")
        return super().parse(data)

class USC55_to_ARKIT_Wrapper(DataFrameWrapper):

    def __init__(self, byteorder: str = 'big') -> None:
        super().__init__(byteorder)

        ARKIT_TO_INDEX = {}
        for index, name in enumerate(NAMES_ARKIT):
            ARKIT_TO_INDEX[name] = index
        
        self._remap_list = [60] * 61
        
        for index, USC55_name in enumerate(sorted(NAMES_USC55)):
            ARKIT_name = NAMES_USC55_from_ARKIT[USC55_name]
            if ARKIT_name != "":
                ARKIT_index = ARKIT_TO_INDEX[ARKIT_name]
                self._remap_list[ARKIT_index] = index
        
    
    def parse(self, data: np.ndarray) -> None:
        # transform from USC55 to ARKIT 61
        # The missing part can be ignored
        if len(data) != 55:
            raise ValueError(f"Error when parsing data frame: it might not be USC55, since the len of data is {len(data)}")
        # print("Origin", data[:5])

        extended_data = np.pad(data, (0, 6), 'constant', constant_values=(0., 0.5))
        ARKIT_data = extended_data[self._remap_list]
        ARKIT_data[-9:] = np.random.randn(9) / 100000
        return super().parse(ARKIT_data)

        # extended_data = np.pad(np.ones(55) / 10, (0, 6), 'constant', constant_values=(0., 0.5))
        # return super().parse(np.ones(61))

        # return super().parse((np.random.randn(61)/10).astype(np.float32))

class BS_Parser():
    
    def __init__(self,
        timecode: Timecode,
        BS_PACKAGE_VER = 6,
        BS_ID = '2BF95C38-D766-4400-8C28-47B55742AE6D',
        DV_NAME = 'iPad',
        byteorder = 'big',
        encoding = 'utf-8',
        dataframe_wrapper: DataFrameWrapper = None
    ) -> None:

        # Data process
        self.timecode = timecode
        self.data_buffer = np.array([])
        self.current_index = 0

        # Data format
        self.byteorder = byteorder
        self.encoding = encoding
        self.float_format = (">" if self.byteorder == 'big' else "<") + "f4"
        if dataframe_wrapper is None:
            self.dataframe_wrapper = DataFrameWrapper(byteorder=self.byteorder)
        else:
            self.dataframe_wrapper = dataframe_wrapper
            self.dataframe_wrapper.set_byteorder(byteorder=self.byteorder)

        # Package info
        self.BS_PACKAGE_VER = BS_PACKAGE_VER
        self.BS_ID = BS_ID
        self.DV_NAME = DV_NAME

        # Convert to bytes
        self.BS_PACKAGE_VER_BYTES = self.BS_PACKAGE_VER.to_bytes(1, byteorder=self.byteorder)
        self.BS_ID_BYTES = self.BS_ID.encode(encoding=self.encoding)
        self.DV_NAME_BYTES = self.DV_NAME.encode(encoding=self.encoding)
        
        self.BS_ID_LEN = len(self.BS_ID_BYTES).to_bytes(4, byteorder=self.byteorder)
        self.DV_NAME_LEN = len(self.DV_NAME_BYTES).to_bytes(4, byteorder=self.byteorder)

        # Package header
        self.PACKAGE_HEADER = self.get_package_header()
    
    def get_package_header(self) -> bytearray:

        package_header = bytearray()

        # Package Header
        package_header.extend(self.BS_PACKAGE_VER_BYTES)
        package_header.extend(self.BS_ID_LEN)
        package_header.extend(self.BS_ID_BYTES)
        package_header.extend(self.DV_NAME_LEN)
        package_header.extend(self.DV_NAME_BYTES)

        return package_header


    
    def parse_npy(self, npy_filename: str) -> None:
        """
        Parse a given npy file into buffer
        
        The npy file should be a Seq_len * BS_NUM of floats
        """

        # Load np file data
        npy_data:np.ndarray = np.load(npy_filename) # Seq_len * BS_NUM of float
        npy_data = npy_data.astype(self.float_format)

        # load data into buffer
        if len(self.data_buffer) == 0:
            self.data_buffer = npy_data
        else:
            self.data_buffer = np.concatenate((self.data_buffer, npy_data), axis=0)
        
    
    def __iter__(self) -> 'BS_Parser':
        return self
    
    def __next__(self) -> bytearray:
        """
        Return first data in buffer into binary package
        """

        if self.current_index >= len(self.data_buffer):
            raise StopIteration

        package = bytearray()

        # Package Header
        package.extend(self.PACKAGE_HEADER)

        # Timecode
        package.extend(self.timecode.get_timecode_bytes())

        # Data
        target_data:np.ndarray = self.data_buffer[self.current_index]
        package.extend(self.dataframe_wrapper.parse(target_data))

        # Update time
        self.current_index += 1
        # self.timecode.__next__()
        print(f"Render id{self.current_index}")

        return package
    
    def clear_buffer(self) -> None:
        """
        Clear the used buffer
        """

        if self.current_index >= len(self.data_buffer):
            self.data_buffer = None
            self.current_index = 0
        else:
            self.data_buffer = self.data_buffer[self.current_index:]
            self.current_index = 0