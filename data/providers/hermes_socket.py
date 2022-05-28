import socket

def encoder(data):
    try:
        return data.encode('utf-8')
    except:
        return data

def decoder(data):
    try:
        return data.decode('utf-8')
    except:
        return data

def get_hostname():
    return socket.gethostbyname(socket.gethostname())

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
    def send(self, message):
        self.socket.send(encoder(message))
    def receive(self):
        return decoder(self.socket.recv(1048576))
    def close(self):
        self.socket.close()

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
    def accept(self):
        self.client, self.address = self.socket.accept()
    def send(self, message):
        self.client.send(encoder(message))
    def receive(self):
        return decoder(self.client.recv(1048576))
    def close(self):
        self.client.close()
        self.socket.close()