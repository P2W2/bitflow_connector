from pathlib import Path
from connector.connector import Connector
import status


class Main:
    def __init__(self, configuration='./configuration'):
        status.init()
        self.config = Path(configuration)
        self.connector = Connector(self.config)


if __name__ == '__main__':
    setts = Main(configuration='./test/config.yml')
