import socket
import keyboard


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 10000)

    def conn(self):
        self.sock.connect(self.server_address)
        try:
            while True:
                data = self.sock.recv(1024).decode('utf-8')
                if data == 'client1':
                    self.cuvant()
                elif data == 'client2':
                    self.ghiceste()
                else:
                    print(data)
                break
        finally:
            self.sock.close()

    def cuvant(self):
        self.sock.sendall(bytes(' ', 'utf-8'))
        message = input(self.sock.recv(1024).decode('utf-8'))
        self.sock.sendall(bytes(message, 'utf-8'))
        message = input(self.sock.recv(1024).decode('utf-8'))
        self.sock.sendall(bytes(message, 'utf-8'))

    def ghiceste(self):
        self.sock.sendall(bytes(' ', 'utf-8'))
        print(self.sock.recv(1024).decode('utf-8'))  # expresia
        while True:
            self.sock.sendall(bytes(input('Dati o litera: '), 'utf-8'))
            message = self.sock.recv(1024).decode('utf-8')
            print(message)
            if 'Ai pierdut' in message or 'Ai castigat' in message:
                break


if __name__ == "__main__":
    client = Client()
    client.conn()
