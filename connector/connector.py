import yaml
from connector.client import Client
import importlib.util
import re
import status
import threading
from connector.clients import Clients


class Connector:
    def __init__(self, path):
        self.settings = self.read_settings(path)
        self.clients = Clients(self.open_clients())
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

    def load_plugins(self):
        plugins = []
        for plugin in self.settings['plugins']:
            plugins.append(importlib.import_module('.'.join(['plugins', 'input', plugin, plugin])))
        return plugins

    def start_plugins(self):
        for plugin_name, module in zip(self.settings['plugins'], self.plugins):
            plugin_class = getattr(module, re.sub(r'([a-zA-Z])_([a-zA-Z])', lambda m: m.group(1).upper(),
                                                  plugin_name.capitalize()))
            x = threading.Thread(target=plugin_class, args=(self.clients, self.settings['plugins'][plugin_name],))
            x.start()

    def open_clients(self):
        cs = {}
        for destination in self.settings['destinations']:
            status.clients.update({destination['name']: {'lock': threading.Lock(), 'reconnect': False}})
            client = Client(destination['name'], self.settings['buffer'], host=destination['host'],
                            port=destination['port'])
            cs.update({destination['name']: client})
        return cs
