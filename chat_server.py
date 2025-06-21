import socket
import threading
import logging

logging.basicConfig(level=logging.INFO)

class ChatServer:
   
    def __init__(self, host='127.0.0.1', port=55555):
       
        self.clients = set()
        # Dicionário para associar o objeto socket ao nome do usuário
        self.nicknames = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.host = host
        self.port = port


    def start(self):
        #Funcao para iniciar o servidor
        self.server_socket.listen()
        logging.info(f"Servidor de Chat (Socket TCP) iniciado em {self.host}:{self.port}")
        
        while True:
            client_socket, address = self.server_socket.accept()
            # Cria e inicia uma nova thread para cada cliente
            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.start() 