#Cliente 
import socket
import threading

def receive_messages(client_socket):
    while True:
        # Receive and display messages from the server
        data = client_socket.recv(1024)
        message = data.decode('utf-8')
        sender_ip, sender_message = message.split(":", 1)
        print(f"Received from {sender_ip.strip()}: {sender_message.strip()}")

# Get the server's IP address and port
server_ip = input("Enter the server's IP address: ")
server_port = 12345

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

while True:
    # Send messages to the server
    message = input()
    client_socket.send(message.encode('utf-8'))

