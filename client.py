import socket
import threading
from plyer import notification  # Import the notification module from plyer

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

# Listening To Server And Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('ascii')

            if message == 'NICK':
                # If 'NICK', Send Nickname
                client.send(nickname.encode('ascii'))
            
            elif message.lower() == f'{nickname}: leave':
                # Notify the user about leaving the chat
                print("You left the chat room.")
                client.close()
                break

            else:
                # Display the received message as a notification (except for own messages)
                sender, _, _ = message.partition(':')
                if sender.lower() != nickname.lower():
                    notification.notify(
                        title=f"New Message from {sender}",
                        message=message,
                        app_name="CL-Chat",  # You can customize this
                        timeout=10,  # Notification will disappear after 10 seconds
                    )

                print(message)
        except:
            # Close Connection When Error
            print("Err...Okay...nvm..LoL")
            client.close()
            break


# Sending Messages To Server
def write():
    while True:
        message = input('You: ')
        if message.lower() == 'leave':
            client.send(message.encode('ascii'))
            print("You left the chat room.")
            client.close()
            break
        else:
            message = '{}: {}'.format(nickname, message)
            client.send(message.encode('ascii'))
            print('\033[F\033[K', end='')  # Clears the input line

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
