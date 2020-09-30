import socket


class Client:
    def __init__(self, host='localhost', port=8080, buffer_size=1024):
        self.buffer_size = buffer_size
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

    def send_sample(self, sample):
        self.s.send(sample)
        #data = self.s.recv(self.buffer_size)
        #return data

    def close_connection(self):
        self.s.close()
