import socket
import threading
import json
from datetime import datetime

# Connection Data
host = '13.200.44.164'  # Replace with your Lightsail instance's public IP or DNS name
port = 7325

# Create a log file
log_file = "chatroom_logs.json"

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client, nickname):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)

            # Log the message
            log_data = {
                "timestamp": str(datetime.now()),
                "nickname": nickname,
                "message": message.decode("ascii").strip()
            }
            with open(log_file, "a") as log_file:
                json.dump(log_data, log_file)
                log_file.write("\n")

        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nicknames.pop(index)
            broadcast('{} left!'.format(nickname).encode('ascii'))
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client, nickname))
        thread.start()

print("Server is listening on {}:{}".format(host, port))
receive()
