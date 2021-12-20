import socket

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 10000)

    def conn(self):
        self.sock.connect(self.server_address)
        try:
            message = ""
            while message != bytes("exit", "utf-8"):
                message = bytes(input("dati text sper server"), 'utf-8')
                self.sock.sendall(message)
                data = self.sock.recv(1024)
                print('primit {!r}'.format(data))
        finally:
            self.sock.close()

if __name__ == "__main__":
    client = Client()
    client.conn()
