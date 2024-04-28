import socket
import pickle

class Network:
    def __init__(self):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 12345
        self.connect()
        self.full_info = pickle.loads(self.socket_client.recv(4096))
        
    def getInfo(self):
        return self.full_info
    
    def connect(self):
        try:
            self.socket_client.connect((self.server, self.port))
        except socket.error as e:
            print("Error when client try to connect to sever")
    
    def send(self, data):
        try:
            self.socket_client.send(pickle.dumps(data))
            return pickle.loads(self.socket_client.recv(4096))
        except socket.error as e:
            print("Error when client try to send data to sever")
        
        