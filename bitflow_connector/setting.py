import yaml
import threading
from prometheus.target_scraper import PromTargetScraper
from bitflow_connector.client import Client


class Settings:
    def __init__(self, path):
        self.settings = self.read_settings(path)
        self.clients = {}
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
        for scraper in self.settings['scrape_configs']:
            if scraper['type'] == 'prometheus':
                if scraper['scrape_interval'] is not None:
                    interval = scraper['scrape_interval']
                else:
                    interval = self.settings['scrape_interval']
                for scrape_target in scraper['scrape_targets']:
                    prom_scraper = PromTargetScraper(self.clients, scrape_target['metrics'], interval,
                                                     target_url=scrape_target['host'] + ':' + scrape_target['port'] +
                                                                scrape_target['path'])

            elif scraper['type'] == 'riemann':
                print('riemann')
            else:
                print('Please set one of the following types for the metrics scraper: riemann, prometheus')

    def open_clients(self):
        for destination in self.settings['destination_configs']:
            client = Client(host=destination['host'], port=destination['port'])
            self.clients.update({destination['name']: client})


if __name__ == '__main__':
    setts = Settings('/home/peewee/workspace/master/bitflow_connector/test/config.yml')
    # print(setts.settings)
    setts.start_scraper()
