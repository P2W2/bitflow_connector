import yaml
from connector.client import Client
import importlib.util
from pathlib import Path
import re

class Connector:
    def __init__(self, path):
        self.settings = self.read_settings(path)
        self.clients = self.open_clients()
        self.scrapers = []
        self.root_path = Path(__file__).parent.parent
        self.plugins = self.load_plugins()
        self.start_plugins()

    @staticmethod
    def read_settings(path):
        with path.open() as stream:
            try:
                yml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return yml

    def to_camelcase(self, s):
        return re.sub(r'([a-zA-Z])_([a-zA-Z])', lambda m: m.group(1).upper(), s.capitalize())

    def load_plugins(self):
        plugins = []
        for plugin in self.settings['plugins']:
            plugins.append(importlib.import_module('.'.join(['plugins', plugin, plugin])))
            return plugins

    def start_plugins(self):
        for plugin_name, module in zip(self.settings['plugins'], self.plugins):
            print(plugin_name, module)
            plugin_class = getattr(module, self.to_camelcase(plugin_name))
            plugin_class(self.clients, self.settings['plugins'][plugin_name])

    def open_clients(self):
        cs = {}
        for destination in self.settings['destinations']:
            client = Client(host=destination['host'], port=destination['port'])
            cs.update({destination['name']: client})
        return cs



