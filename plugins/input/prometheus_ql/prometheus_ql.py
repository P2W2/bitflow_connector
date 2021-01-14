import threading
import requests
import time


class PrometheusQl(threading.Thread):
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
                #self.forward(data)
            time.sleep(self.settings['scrape_interval'])
        pass

    def get_data(self, target):
        ret = requests.get(target['protocol'] + '://' + target['host'] + ':' + str(target['port']) + '/api/v1/query', params={
            'query': '{__name__=~"' + '|'.join(self.settings['metrics']) + '"}'}).json()
        return ret

    def forward(self, data):
        for destination in self.settings['metric_destinations']:
            self.clients[destination].send_sample(data)

    def bitflow_csv_converter(self, data):
        print(data)
        print(self.settings['metrics'])
        return None


if __name__ == '__main__':
    scraper = PrometheusQl('bla', 'bla')
    r = scraper.biflow_csv_converter(['cpu_percent', 'virtual_memory_percent'],
                                     'http://localhost:9090')
