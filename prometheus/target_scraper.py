import re
import json
import requests


class PromTargetScraper:
    def __init__(self, destinations, metrics, scrape_interval=500, target_url='localost/metrics'):
        self.target = target_url

    def get_json_metrics(self, metric_keys):
        r = requests.get(self.target)
        metric_dict = {}
        for m in re.sub(r'(?m)^ *#.*\n?', '', r.text).split('\n'):
            m = m.split()
            if len(m) == 2 and m[0] in metric_keys:
                metric_dict.update({m[0]: m[1]})
        return json.dumps(metric_dict)

    def get_csv_metrics(self, metric_keys):
        r = requests.get(self.target)
        keys = []
        metrics = []
        for m in re.sub(r'(?m)^ *#.*\n?', '', r.text).split('\n'):
            m = m.split()
            if len(m) == 2 and m[0] in metric_keys:
                keys.append(m[0])
                metrics.append(m[1])
        return ', '.join(keys) + '\n' + ', '.join(metrics)

    def scrape(self):


if __name__ == '__main__':
    scraper = PromTargetScraper('bla', 'bla', target_url='http://0.0.0.0:5000/metrics')
    ret = scraper.get_csv_metrics(['cpu_percent',
                                   'virtual_memory_percent'])
    print(ret)
