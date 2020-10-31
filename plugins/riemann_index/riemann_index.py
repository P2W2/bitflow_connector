import bernhard
import threading
import requests
import time


class RiemannIndex(threading.Thread):
    def __init__(self, clients, settings):
        super().__init__()
        self.clients = clients
        self.settings = settings
        self.running = True
        self.run()

    def run(self):
        while self.running:
            for target in self.settings['targets']:
                data = self.bitflow_csv_converter(self.get_data(target))
                # self.forward(data)
            time.sleep(self.settings['scrape_interval'])
        pass

    def get_data(self, target):
        c = bernhard.Client(host=target['protocol'] + '://' + target['host'], port=target['port'])
        return c.query('host = "peewee-ThinkPad"')

    def forward(self, data):
        for destination in self.settings['metric_destinations']:
            self.clients[destination].send_sample(data)

    def bitflow_csv_converter(self, data):
        print(data)
        print(self.settings['metrics'])
        return None
