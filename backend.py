import socket
import threading
import time
from pymongo import MongoClient  # Import MongoClient from pymongo

# Connection Data
host = 'your-server-ip'
port = #your server port

# MongoDB Connection URI
mongo_uri = "" #your mongodb uri
client = MongoClient(mongo_uri)
db = client["cl-chat"]  # Replace "chat_log_db" with your desired database name
chat_log_collection = db["chat_log"]  # Replace "chat_log" with your desired collection name

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message, sender):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} {sender}: {message}"
    chat_log_collection.insert_one({"timestamp": timestamp, "sender": sender, "message": message})
    for client in clients:
        try:
            client.send(log_entry.encode('ascii'))
        except:
            # Remove and close the client if there's an error
            remove_client(client)

# Remove and Close Client
def remove_client(client):
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        clients.remove(client)
        nicknames.remove(nickname)
        client.close()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} {nickname} left the chat."
        chat_log_collection.insert_one({"timestamp": timestamp, "sender": "Server", "message": f"{nickname} left the chat."})
        broadcast('{} left!'.format(nickname), "Server")

# Handling Messages From Clients
def handle(client, nickname):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024).decode('ascii')
            if not message:
                break
            broadcast(message, nickname)

        except:
            # Remove and close the client if there's an error
            remove_client(client)

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
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} {nickname} joined the chat."
        chat_log_collection.insert_one({"timestamp": timestamp, "sender": "Server", "message": f"{nickname} joined the chat."})
        broadcast("{} joined!".format(nickname), "Server")
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client, nickname))
        thread.start()

print("Server is listening on {}:{}".format(host, port))
receive()
