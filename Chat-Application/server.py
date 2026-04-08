import socket
import threading

host = '127.0.0.1'
port = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

clients = []

print("Server running...")

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            client.close()
            clients.remove(client)

def handle_client(conn, addr):
    print(f"Connected: {addr}")
    clients.append(conn)

    while True:
        try:
            message = conn.recv(1024)
            if not message:
                break
            broadcast(message)
        except:
            break

    print(f"Disconnected: {addr}")
    clients.remove(conn)
    conn.close()

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
