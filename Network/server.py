#Server
import socket
import threading

# Dictionary to store the number of requests from each client
client_requests = {}

def handle_client(client_socket, client_address):
    # Display client information
    print(f"Accepted connection from {client_address}")

    while True:
        # Receive message from the client
        data = client_socket.recv(1024)

        if not data:
            break

        # Display and broadcast the message to all clients
        sender_ip = client_address[0]
        message = data.decode('utf-8')
        print(f"Received from {client_address}: {message}")
        broadcast(f"{sender_ip}: {message}", client_socket)

        # Update the number of requests from the client
        client_ip = client_address[0]
        client_requests[client_ip] = client_requests.get(client_ip, 0) + 1

    # Remove the client's IP from the dictionary when the client disconnects
    del client_requests[client_ip]
    print(f"Connection from {client_address} closed")

def broadcast(message, sender_socket):
    for client_socket in client_sockets:
        if client_socket != sender_socket:
            client_socket.send(message.encode('utf-8'))

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind(('0.0.0.0', 12345))

# Listen for incoming connections
server_socket.listen(5)

print("Server listening on port 12345")

# List to store client sockets
client_sockets = []

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()

    # Add the client socket to the list
    client_sockets.append(client_socket)

    # Create a thread to handle the client
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()

