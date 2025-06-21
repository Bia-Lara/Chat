import socket
import threading
import logging

logging.basicConfig(level=logging.INFO)

class ChatServer:
   
    def __init__(self, host='127.0.0.1', port=55555):
        
        self.clients = set()
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
            client_socket, _ = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.start()

    def broadcast(self, message, sender_socket=None):
       #Funcao para enviar a mensagem para todos os clientes conectados
       

    def handle_client(self, client_socket):
       #Funcao para lidar com a comunicação de um cliente individualmente
        nickname = None
        try:
            nickname, message_buffer = self._perform_login(client_socket)
            if nickname:
                self._listen_for_messages(client_socket, nickname, message_buffer)
        except (ConnectionResetError, ConnectionError) as e:
            logging.info(f"Conexão com {nickname or 'cliente desconhecido'} perdida: {e}")
        finally:
            self._cleanup_client(client_socket)

    def _perform_login(self, client_socket):
       #Funcao para realizar o "login" do cliente
        client_socket.send(b'Bem-vindo! Por favor, digite seu nome de usuario e pressione Enter:\n')
        
        buffer = b""
        while b'\n' not in buffer:
            data = client_socket.recv(1024)
            if not data: raise ConnectionError("Desconectou antes de fornecer um nome.")
            buffer += data
        
        nickname_bytes, message_buffer = buffer.split(b'\n', 1)
        nickname = nickname_bytes.decode('utf-8').strip()

        if not nickname:
            nickname = f"Usuario_{client_socket.getpeername()[1]}"
            client_socket.send(f"\rNome invalido. Seu nome sera '{nickname}'.\n".encode('utf-8'))

        self.clients.add(client_socket)
        self.nicknames[client_socket] = nickname
        logging.info(f"'{nickname}' conectou-se de {client_socket.getpeername()}.")

        join_message = f"\r'{nickname}' entrou no chat!\n".encode('utf-8')
        self.broadcast(join_message, client_socket)
        
        return nickname, message_buffer

    def _listen_for_messages(self, client_socket, nickname, message_buffer):
       #Funcao para escutar as mensagens do cliente
        while True:
            while b'\n' in message_buffer:
                message_bytes, message_buffer = message_buffer.split(b'\n', 1)
                message_text = message_bytes.decode('utf-8').strip()
                if message_text:
                    formatted_message = f"\r{nickname}: {message_text}\n".encode('utf-8')
                    self.broadcast(formatted_message, client_socket)

            data = client_socket.recv(1024)
            if not data: break
            message_buffer += data

    def _cleanup_client(self, client_socket):
        #Funcao para limpar o cliente
        if client_socket in self.clients:
            nickname = self.nicknames.pop(client_socket)
            self.clients.remove(client_socket)
            client_socket.close()
            
            logging.info(f"'{nickname}' desconectou-se.")
            
            leave_message = f"\r'{nickname}' saiu do chat.\n".encode('utf-8')
            self.broadcast(leave_message) 