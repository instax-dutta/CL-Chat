import socket
import threading
from plyer import notification

# Connection Data
host = 'chat.bunk.pro'
port = 8080
print(r""" #$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#
   ____ _           ____ _   _    _  _____ 
  / ___| |         / ___| | | |  / \|_   _|
 | |   | |   _____| |   | |_| | / _ \ | |  
 | |___| |__|_____| |___|  _  |/ ___ \| |  
  \____|_____|     \____|_| |_/_/   \_\_|  
            By Abhishek Dash
#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#                                     
     """)
# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Prompting The Client For A Nickname
nickname = input("Choose your nickname: ")

# Flag to track if connected notification has been sent
connected_notification_sent = False

# Listening To Server And Sending Nickname
def receive():
    global connected_notification_sent
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('ascii')

            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                # Send connected notification only once
                if not connected_notification_sent:
                    connected_notification_sent = True

            else:
                # Check if the message is "leave" to exit the chat
                if message.lower() == f'{nickname}: leave':
                    print("You left the chat room.")
                    client.close()
                    break
                else:
                    # Display the received message without timestamp
                    sender, _, received_message = message.partition(':')
                    # Exclude server-related messages
                    if sender.lower() != "server" and received_message.lower().strip() != "get / http/1.1":
                        print(f"{sender}: {received_message.strip()}")  # Print the message without timestamp

                        # Display notification for others' messages
                        if sender.lower() != nickname.lower():
                            # Check for join and exit messages
                            if received_message.endswith("joined the chat.") or received_message.endswith("left the chat."):
                                notification.notify(
                                    title="CL-Chat Notification",
                                    message=received_message,
                                    app_name="CL-Chat",
                                    timeout=10,
                                )
                            else:
                                # Display notification for others' messages
                                notification.notify(
                                    title=f"New Message from {sender}",
                                    message=received_message,
                                    app_name="CL-Chat",
                                    timeout=10,
                                )

        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        message = input('')  # Empty string to prevent displaying the input prompt
        if message.lower() == 'leave':
            client.send(f'{nickname}: leave'.encode('ascii'))
            print("You left the chat room.")
            client.close()
            break
        else:
            client.send(f'{nickname}: {message}'.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
