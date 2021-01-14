import plugins.input.riemann.proto.proto_pb2 as pb
from plugins.input.riemann.simpletcp.tcpserver import TCPServer
from datetime import datetime


class Riemann:
    def __init__(self, clients, settings):
        print('----Start Riemann Plugin----')
        self.REPLY = b'\x00\x00\x00\x02\x10\x01'
        self.clients = clients
        self.settings = settings
        self.fields = {
            'time': lambda x, y, z: x.update({'time': datetime.fromtimestamp(z)}),
            'tags': self.tags_field,
            'ttl': lambda x, y, z: x['metrics'].update({'ttl': z}),
            'metric': lambda x, y, z: x['metrics'].update({y.service: z}),
            'metric_f': lambda x, y, z: x['metrics'].update({y.service: z}),
            'metric_d': lambda x, y, z: x['metrics'].update({y.service: z}),
            'metric_sint64': lambda x, y, z: x['metrics'].update({y.service: z}),
            'attributes': self.attr_field
        }
        self.run()

    def run(self):
        server = TCPServer(self.settings['host'], self.settings['port'], self.receive)
        print('Server starts listening on ' + self.settings['host'] + ':' + str(self.settings['port']))
        server.run()

    def receive(self, ip, queue, msg):
        queue.put(self.REPLY)
        data = pb.Msg()
        data.ParseFromString(msg[4:])
        data = self.bitflow_csv_converter(data)
        #print(data)
        self.clients.send_samples(data, self.settings['metric_destinations'])

    def bitflow_csv_converter(self, data):
        metrics = []
        for event in data.events:
            js = {'tags': {}, 'metrics': {}, 'time': datetime.now()}
            for field, value in event.ListFields():
                self.fields.get(field.name, lambda x, y, z: x['tags'].update({str(field.name): z}))(
                    js, event, value)
            metrics.append(js)
        return metrics

    def attr_field(self, js, event, value):
        for a in value:
            js['tags'].update({a.key: a.value})

    def tags_field(self, js, event, value):
        for t in value:
            js['tags'].update({'tag_' + str(t): t})
