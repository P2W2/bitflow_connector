import socket
import time


class Client:
    def __init__(self, host='localhost', port=8080, buffer_size=1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        self.connected = True

    def send_sample(self, sample):
        try:
            self.s.send(sample.encode())
        except socket.error:
            connected = False
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("connection lost... reconnecting")
            while not connected:
                try:
                    self.s.connect((self.host, self.port))
                    connected = True
                    print("re-connection successful")
                except socket.error:
                    time.sleep(1)

    def close_connection(self):
        self.s.close()
