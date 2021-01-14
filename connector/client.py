import socket
import time
import threading
import status
import pandas


class Client:
    def __init__(self, name, buffer, host='localhost', port=8080, buffer_size=1024):
        self.name = name
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.s = self.start_connect()
        self.connected = True

    def send(self, samples):
        message = self.create_message(samples)
        try:
            self.s.send(message.encode())
        except socket.error:
            self.reconnecting()

    def create_message(self, samples):
        dfs = pandas.DataFrame()
        for sample in samples:
            sample_dic = {'time': str(sample['time'])}
            tags = ''
            for tag in sample['tags'].keys():
                tags = tags + tag + '=' + str(
                    sample['tags'][tag]).replace(' ', '_').replace(',', '_').replace('=', '_').replace('\n', '_') + ' '
            sample_dic.update({'tags': tags[:-1]})
            for m in sample['metrics'].keys():
                sample_dic.update({m: sample['metrics'][m]})
            s_df = pandas.DataFrame([sample_dic])
            dfs = dfs.append(s_df, sort=False, ignore_index=True)
        return dfs.to_csv(index=False)

    def start_connect(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))
        except socket.error:
            x = threading.Thread(target=self.reconnecting, args=())
            x.start()
        return self.s

    def reconnecting(self):
        # TODO Clean up mess
        connected = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not status.clients[self.name]['reconnect']:
            status.clients[self.name]['lock'].acquire()
            status.clients[self.name]['reconnect'] = True
            print('start reconnecting')
            while not connected and status.clients[self.name]['reconnect']:
                try:
                    self.s.connect((self.host, self.port))
                    connected = True
                    print("re-connection successful")
                except socket.error:
                    time.sleep(1)
            status.clients[self.name]['reconnect'] = False
            status.clients[self.name]['lock'].release()
            self.buffer.send_saved()

    def send_sample(self, samples):
        x = threading.Thread(target=self.send, args=(samples,))
        x.start()

    def close_connection(self):
        self.s.close()
