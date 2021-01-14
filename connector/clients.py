class Clients:
    def __init__(self, clients):
        self.clients = clients

    def send_samples(self, data, destinations):
        for destination in destinations:
            self.clients[destination].send_sample(data)
