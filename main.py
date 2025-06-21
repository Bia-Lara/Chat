from chat_server import ChatServer

# --- Configurações do Servidor ---
HOST = '127.0.0.1'
PORT = 55555

def main():
    server = ChatServer(HOST, PORT)
    server.start()

if __name__ == "__main__":
    main() 