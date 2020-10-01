import yaml
import threading
from prometheus.target_scraper import PromTargetScraper
from riemann.input_stream import RiemannInputStream
from bitflow_connector.client import Client


class Settings:
    def __init__(self, path):
        self.settings = self.read_settings(path)
        self.clients = self.open_clients()
        self.scrapers = []

    @staticmethod
    def read_settings(path):
        with open(path, 'r') as stream:
            try:
                yml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return yml

    def start_scraper(self):
        # if self.settings['prometheus']:
        #     for scrape_target in self.settings['prometheus']['scrape_targets']:
        #             prom_scraper = PromTargetScraper(self.clients, scrape_target['metrics'], scrape_target['scrape_interval'],
        #                                              target_url=scrape_target['host'] + ':' + scrape_target['port'] +
        #                                                         scrape_target['path'])

        if self.settings['riemann_stream']:
            riemann_scraper = RiemannInputStream(self.clients, self.settings['riemann_stream'])
        else:
            print('Please set one of the following types for the metrics scraper: riemann, prometheus')

    def open_clients(self):
        cs = {}
        for destination in self.settings['destination_configs']:
            client = Client(host=destination['host'], port=destination['port'])
            cs.update({destination['name']: client})
        return cs


if __name__ == '__main__':
    setts = Settings('/home/peewee/workspace/master/bitflow_connector/test/config.yml')
    # print(setts.settings)
    setts.start_scraper()
