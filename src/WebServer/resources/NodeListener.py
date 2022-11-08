import socket
import multiprocessing


class UDPSocket:

    def __init__(self) -> None:
        self.name = "listener"
        self.route = "/api/listener/<string:test>"

        self.port = 1337
        self.ip = socket.gethostbyname(socket.gethostname())

        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind(("192.168.99.197", self.port))

    def __listen_to_socket(self, *args) -> None:
        while True:
            print(self.socket.recv(1024))

    def start_process(self):
        p = multiprocessing.Process(target=self.__listen_to_socket, args=(self, ))
        p.start()
        p.join()

