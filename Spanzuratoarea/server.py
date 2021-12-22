import socket
import threading


class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = ('localhost', 10000)
        self.max_clients = 0  # maxim 2 clienti vor fi conectati la server
        self.sock.bind(self.server_address)
        self.word = ''
        self.exp = ''
        self.connection1 = ''
        self.connection2 = ''

    def listen(self):
        self.sock.listen(5)
        while True:
            connection, client_address = self.sock.accept()
            threading.Thread(target=self.listen_to_client, args=(connection, client_address)).start()

    def listen_to_client(self, connection, client_address):
        while True:
            try:
                self.max_clients += 1
                if self.max_clients > 2:
                    connection.sendall(bytes('Serverul este full', 'utf-8'))
                else:
                    nr_client = self.max_clients  # primul client da cuvantul, al doailea incearca sa il ghiceasca
                    while True:
                        if self.max_clients == 2:
                            if nr_client == 1:
                                self.connection1 = connection
                                self.cuvant()
                            elif nr_client == 2:
                                self.connection2 = connection
                                self.ghiceste()
                            break
            finally:
                connection.close()

    def ghiceste(self):
        self.connection2.sendall(bytes('client2', 'utf-8'))
        self.connection2.recv(1024)
        incercari = int(len(self.word) / 2 + 1)
        self.connection2.sendall(bytes(self.exp, 'utf-8'))
        aux = self.new_word()
        while True:
            message = ''
            ok = 0
            character = self.connection2.recv(1024).decode('utf-8')
            if character in self.word:
                nr = self.word.count(character)
                for i in range(nr):
                    index = self.word.index(character)
                    aux = aux[0:index] + self.word[index] + aux[index + 1:]
                    self.word = self.word.replace(character, '_', 1)
                if aux.count('_') == 0:
                    ok = 1
                    message = '\nAi castigat'
                self.connection2.sendall(bytes(aux + message, 'utf-8'))
                if ok == 1:
                    break
            else:
                incercari -= 1
                print(incercari)
                message1 = '\nMai ai ' + "% s" % incercari + ' incercari'
                message2 = '\nAi pierdut'
                if incercari == 0:
                    ok = -1
                if ok == -1:
                    self.connection2.sendall(bytes(aux + message2, 'utf-8'))
                    break
                else:
                    self.connection2.sendall(bytes(aux + message1, 'utf-8'))

    def new_word(self):
        index = 0
        aux = ''
        while index < len(self.word):
            aux += "_"
            index += 1
        return aux

    def cuvant(self):
        self.connection1.sendall(bytes('client1', 'utf-8'))
        self.connection1.recv(1024)
        self.connection1.sendall(bytes('Dati cuvantul: ', 'utf-8'))
        self.word = self.connection1.recv(1024).decode('utf-8')
        self.connection1.sendall(bytes('Dati o mica definitie a cuvantului: ', 'utf-8'))
        self.exp = self.connection1.recv(1024).decode('utf-8')


if __name__ == "__main__":
    server = Server()
    server.listen()
