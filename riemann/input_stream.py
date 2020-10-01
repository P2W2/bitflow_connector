import riemann.proto.proto_pb2 as pb
from riemann.simpletcp.tcpserver import TCPServer
from datetime import datetime


class RiemannInputStream:
    def __init__(self, clients, settings, buffer_size=4096):
        self.clients = clients
        self.settings = settings
        server = TCPServer(self.settings['host'], self.settings['port'], self.receive)
        server.run()

    def receive(self, ip, queue, data):
        print("received data:", data[4:])
        msg = pb.Msg()
        msg.ParseFromString(data[4:])
        self.forward(msg)
        queue.put(data)

    def forward(self, msg):
        sample = self.get_csv_metrics(msg)
        for destinantion in self.settings['metric_destinations']:
            self.clients[destinantion].send_sample(sample)

    def get_csv_metrics(self, message):
        csv_header = 'time,tags'
        if message.events[0].service:
            csv_header += ',' + message.events[0].service
        elif message.events[0].metric or message.events[0].metric_f or message.events[0].metric_d:
            csv_header += ',metric'

        csv_sample = '' + str(datetime.fromtimestamp(message.events[0].time)) + ','
        if message.events[0].host:
            csv_sample += 'host=' + message.events[0].host
        if message.events[0].state:
            csv_sample += ' state=' + message.events[0].state
        if message.events[0].description:
            csv_sample += ' description=' + message.events[0].description
        if message.events[0].tags:
            csv_sample += ' tags=' + str(message.events[0].tags)
        if message.events[0].ttl:
            csv_sample += ' ttl=' + str(message.events[0].ttl)
        if hasattr(message.events[0], 'metric'):
            csv_sample += ',' + str(message.events[0].metric)
        elif hasattr(message.events[0], 'metric_f'):
            csv_sample += ',' + str(message.events[0].metric_f)
        elif hasattr(message.events[0], 'metric_d'):
            csv_sample += ',' + str(message.events[0].metric_d)

        return csv_header + '\n' + csv_sample + '\n'
