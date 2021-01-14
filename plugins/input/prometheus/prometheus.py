import re
import requests
import threading
import time
import datetime


class Prometheus(threading.Thread):
    def __init__(self, clients, settings):
        print('----Start Prometheus Plugin----')
        super().__init__()
        self.clients = clients
        self.settings = settings
        self.running = True
        self.run()

    def run(self):
        while self.running:
            for target in self.settings['targets']:
                data = self.bitflow_csv_converter(self.get_data(target))
                self.forward(data)
            time.sleep(self.settings['scrape_interval'])

    def get_data(self, target):
        print('TARGET:', target)
        print(hasattr(target, 'port'))
        if target.__contains__('port'):
            target = target['protocol'] + '://' + target['host'] + ':' + str(target['port']) + target['path']
        else:
            target = target['protocol'] + '://' + target['host'] + target['path']
        return requests.get(target), target

    def forward(self, data):
        print('send data:', data)
        self.clients.send_samples(data, self.settings['metric_destinations'])
        print('-------------------')

    def bitflow_csv_converter(self, data):
        data, target = data[0], data[1]
        keys = []
        metrics = []
        for m in re.sub(r'(?m)^ *#.*\n?', '', data.text).split('\n'):
            m = m.split()
            if len(m) == 2 and m[0] in self.settings['metrics']:
                keys.append(m[0])
                metrics.append(m[1])
        keys = ['time', 'tags'] + keys
        metrics = [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), 'target=' + target] + metrics
        return ','.join(keys) + '\n' + ','.join(metrics)


if __name__ == '__main__':
    scraper = Prometheus(target_url='http://0.0.0.0:5000/metrics')
    ret = scraper.biflow_csv_converter(['cpu_percent',
                                        'virtual_memory_percent'])
    print(ret)
