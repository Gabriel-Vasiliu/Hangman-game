import socket

class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 10000)
        self.max_clients = 2
        self.sock.bind(self.server_address)

    def listen(self):
        self.sock.listen(self.max_clients)

        while True:
            connection, client_addr = self.sock.accept()
            try:
                data = ""
                while data != bytes("exit", "utf-8"):
                    data = connection.recv(1024)
                    if data == bytes("exit", "utf-8"):
                        print("exit de la client")
                    print('primit data cu format {!r}'.format(data))
                    print('sent to client')
                    connection.sendall(b'de la server')
            finally:
                connection.close()

if __name__ == "__main__":
    server = Server()
    server.listen()