import plugins.riemann.proto.proto_pb2 as pb
from plugins.riemann.simpletcp.tcpserver import TCPServer
from datetime import datetime


class Riemann:
    def __init__(self, clients, settings, buffer_size=4096):
        print('----Start Riemann Plugin----')
        self.clients = clients
        self.settings = settings
        self.run()

    def run(self):
        server = TCPServer(self.settings['host'], self.settings['port'], self.receive)
        print('Server starts listening on ' + self.settings['host'] + ':' + str(self.settings['port']))
        server.run()

    def receive(self, ip, queue, msg):
        data = self.biflow_csv_converter(self.get_data(msg))
        self.forward(data)
        queue.put(data)

    def get_data(self, msg):
        data = pb.Msg()
        data.ParseFromString(msg[4:])
        if not any(item in [data.events[0].service, 'metric', 'metric_d', 'metric_f'] for item in self.settings['metrics']):
            print('No metrics in message')
            return False
        return data

    def forward(self, data):
        if data:
            print('forward:', data)
            print(data)
            for destination in self.settings['metric_destinations']:
                self.clients[destination].send_sample(data)

    def bitflow_csv_converter(self, data):
        csv_header = 'time,tags'
        if data.events[0].service:
            csv_header += ',' + data.events[0].service
        elif data.events[0].metric or data.events[0].metric_f or data.events[0].metric_d:
            csv_header += ',metric'

        csv_sample = '' + str(datetime.fromtimestamp(data.events[0].time)) + ','
        if data.events[0].host:
            csv_sample += 'host=' + data.events[0].host
        if data.events[0].state:
            csv_sample += ' state=' + data.events[0].state
        if data.events[0].description:
            csv_sample += ' description=' + data.events[0].description
        if data.events[0].tags:
            csv_sample += ' tags=' + str(data.events[0].tags)
        if data.events[0].ttl:
            csv_sample += ' ttl=' + str(data.events[0].ttl)
        if hasattr(data.events[0], 'metric'):
            csv_sample += ',' + str(data.events[0].metric)
        elif hasattr(data.events[0], 'metric_f'):
            csv_sample += ',' + str(data.events[0].metric_f)
        elif hasattr(data.events[0], 'metric_d'):
            csv_sample += ',' + str(data.events[0].metric_d)

        return csv_header + '\n' + csv_sample + '\n'
