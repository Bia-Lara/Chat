# Backend do Chat em Python (Socket TCP)

Este é o backend para um sistema de chat em tempo real, construído com Python usando uma arquitetura orientada a objetos e **sockets TCP puros**. Ele foi projetado para ser modular e robusto.

**Atenção:** No estado atual funciona com clientes de terminal, como `telnet` ou `netcat`.

## Estrutura do Projeto

- **`main.py`**: Este é o ponto de entrada da aplicação. Sua única responsabilidade é configurar o host e a porta, instanciar a classe `ChatServer` e iniciar o servidor.
- **`chat_server.py`**: O coração da aplicação. Contém a classe `ChatServer`, que gerencia os clientes conectados, lida com múltiplas conexões usando `threading`, e gerencia o ciclo de vida da comunicação.

## Como Executar

1.  **Inicie o servidor:**
    ```bash
    python main.py
    ```
    Você verá a mensagem: `INFO:root:Servidor de Chat (Socket TCP) iniciado em 127.0.0.1:55555`.

2.  **Conecte clientes:**
    Abra **novos terminais** para cada cliente e use o `telnet`:
    ```bash
    telnet 127.0.0.1 55555
    ```

---

