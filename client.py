import socket
import threading

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
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(nickname, input('You: '))
        client.send(message.encode('ascii'))
        print('\033[F\033[K', end='')  # Clears the input line

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
