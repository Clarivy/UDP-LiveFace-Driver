import socket
import threading
import time
import typing

class UDP_Sender():

    def __init__(self, IP: str, port: int) -> None:
        self.IP = IP
        self.port = port
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def send(self, bytesToSend: bytes):
        self.UDPClientSocket.sendto(bytesToSend, (self.IP, self.port))

class UDP_Reciever():

    def __init__(self, IP: str, port: int, bufferSize: int = 65532, logger: typing.TextIO = None) -> None:
        self.IP = IP
        self.port = port
        self.bufferSize = bufferSize
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.thread = None
        self.logger = logger
    
    def _serve(self) -> None:
        self.UDPClientSocket.bind((self.IP, self.port))
        print("UDP server up and listening")
        while True:
            bytesAddressPair = self.UDPClientSocket.recvfrom(self.bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            clientIP  = "Client IP Address:\n{}".format(address)
            clientMsg = "Message from Client:\n{}".format(message.hex())
            print(clientIP)
            print(clientMsg)
            if self.logger is not None:
                self.logger.write(message)
    

    
    def serve(self) -> None:
        if self.thread is not None:
            raise Exception("Already serving")
        print("Starting server tread")
        self.thread = threading.Thread(target=self._serve, daemon=True, name="UDP server thread")
        self.thread.start()