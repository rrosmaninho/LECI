#!/usr/bin/python3

import sys
import csv
import json
import random
import socket
import select
import base64
#from Crypto.Cipher import AES
#from Crypto.Hash import SHA256
#from common_comm import send_dict, recv_dict, sendrecv_dict

# Dictionary with client information
users = {}


# Returns the client_id of a socket or None
def find_client_id(client_socket):
	for key in users.keys():
		if users[key]["socket"] == client_socket: return key
	return None


# Support for the elimination of a client
# Obtains the client_id from his socket and delete from the dictionary
def clean_client(client_socket):
	client_id = find_client_id(client_socket)
	if client_id != None:
		print("Client %s removed\n" % client_id)
		del users[client_id]


# Returns int data encrypted in a 16 bytes binary string and coded base64
def encrypt_intvalue(client_id, data):
	return str(base64.b64encode(users[client_id]["cipher"].encrypt(bytes("%16d" % (data), "utf8"))), "utf8")


# Returns int data decrypted from a 16 bytes binary string and coded base64
def decrypt_intvalue(client_id, data):
	return int(str(users[client_id]["cipher"].decrypt(base64.b64decode(data)), "utf8"))


# Support for the creation of a csv file with it's respective headline
def create_file():
	with open("result.csv", "w", newline="") as csvfile:
		fw = csv.DictWriter(csvfile, fieldnames=["client_id", "number_of_numbers", "guess"], delimiter=",")
		fw.writeheader()


# Support for the created csv file update
def update_file(client_id, size, guess):
	with open("result.csv", "a", newline="") as csvfile: 
		csv.writer(csvfile).writerow([client_id, size, guess])
		csvfile.close()


# Returns int value and list of description strings identifying the characteristic of the generated value
def generate_result(list_values):
	if len(list_values) % 2 == 1: test = 4
	else : test = 3

	minimal = min(list_values)
	maximal = max(list_values)
	first = list_values[0]
	last = list_values[-1]
		
	choice = random.randint(0, test)
	if choice == 0:
		if minimal == first: return first, ["min", "first"]
		elif maximal == first: return first, ["max", "first"]
		else: return first, ["first"]
	elif choice == 1:
		if minimal == last: return last, ["min", "last"]
		elif maximal == last: return last, ["max", "last"]
		else: return last, ["last"]
	elif choice == 2:
		if minimal == first: return first, ["min", "first"]
		elif minimal == last: return last, ["min", "last"]
		else: return minimal, ["min"]
	elif choice == 3:
		if maximal == first: return first, ["max", "first"]
		elif maximal == last: return last, ["max", "last"]
		else: return maximal, ["max"]
	elif choice == 4:
		list_values.sort()
		median = list_values[len(list_values) // 2]
		if median == first: return first, ["median", "first"]
		elif median == last: return last, ["median", "last"]
		else: return median, ["median"]
	else: return None


# Support for decoding client's wanted operation
def new_msg(client_socket):
	request = 2
	op = request["op"]
	if op == "START": response = new_client(client_socket, request)
	elif op == "QUIT": response = quit_client(client_socket, request)
	elif op == "NUMBER": response = number_client(client_socket, request)
	elif op == "STOP": response = stop_client(client_socket, request)
	elif op == "GUESS": response = guess_client(client_socket, request)
	else: response = { "op": op, "status" : False, "error": "Operação inexistente" }
	#send_dict(client_socket, response )


# ----- START -----
# Support for creating new clients
# Detects the client in the request
# Adds the client in the dictionary with or without cipher
# Returns a response message with or without error message
def new_client(client_socket, request):
	if request["client_id"] not in users:
		cipher = request["cipher"]
		#if cipher != None: cipher = AES.new(base64.b64decode(cipher), AES.MODE_ECB)
		users[request["client_id"]] = {"socket" : client_socket, "cipher" : cipher}
		return { "op": "START", "status": True }
	return { "op": "START", "status": False, "error": "Cliente existente" }


# ----- QUIT -----
# Support for the withdrawal of a client
# Obtains the client_id from his socket
# Eliminates client from dictionary using the function clean_client
# Returns a response message with or without error message
def quit_client(client_socket, request):
	client_id = find_client_id(client_socket)
	if client_id != None:
		clean_client(client_socket)
		return { "op": "QUIT", "status": True }
	return { "op": "QUIT", "status": False, "error": "Cliente inexistente" }


# ----- NUMBER -----
# Support for the client's given number process
# Obtains the client_id from his socket and checks for client's cipher option
# Adds the processed number to the client's number list, if no list is found, creates the list and adds the number
# Returns a response message with or without error message
def number_client(client_socket, request):
	client_id = find_client_id(client_socket)
	if client_id != None:
		if users[client_id]["cipher"] != None: users[client_id]["numbers"] = users[client_id].get("numbers", []) + [decrypt_intvalue(client_id, request["number"])]
		elif users[client_id]["cipher"] == None: users[client_id]["numbers"] = users[client_id].get("numbers", []) + [request["number"]]
		return { "op": "NUMBER", "status": True }
	return { "op": "NUMBER", "status": False, "error": "Cliente inexistente" }


# ----- STOP -----
# Support for the end of number inputs
# Obtains the client_id from his socket
# Randomly generate a value to return using the function generate_result
# Updates the csv file using the function update_file, and changes client's information for better usage of guess_client function
# Returns a response message with result or error message, checking for client's cipher option
def stop_client(client_socket, request):
	client_id = find_client_id(client_socket)
	if client_id != None:
		if users[client_id].get("numbers") == None: return { "op": "STOP", "status": False, "error": "Dados insuficientes" }
		value, users[client_id]["solutions"] = generate_result(users[client_id]["numbers"])
		update_file(client_id, len(users[client_id]["numbers"]), users[client_id]["solutions"])
		if users[client_id]["cipher"] != None: return { "op": "STOP", "status": True, "value" : encrypt_intvalue(client_id, value)}
		elif users[client_id]["cipher"] == None: return { "op": "STOP", "status": True, "value" : value}
	return { "op": "STOP", "status": False, "error": "Cliente inexistente" }


# ----- GUESS -----
# Support for the client's guess
# Obtains the client_id from his socket
# Checks if client's guess is a solution and eliminates client from dictionary
# Returns a response message with result or error message
def guess_client(client_socket, request):
	client_id = find_client_id(client_socket)
	if client_id != None: 
		guess = request["choice"] in users[client_id]["solutions"]
		clean_client(client_socket)
		return { "op": "GUESS", "status": True, "result": guess }
	return { "op": "GUESS", "status": False, "error": "Cliente inexistente" }


def main(argvs):
	if not len(argvs) == 2: # Validates the number of arguments, prints error message and exits with error
		print("Usage: python3 server.py socket")
		sys.exit(1)
	elif not (argvs[1].isdigit() and int(argvs[1]) >= 0): # Validates the port argument, prints error message and exits with error
		print("Socket must be a positive integer!")
		sys.exit(2)

	port = int(argvs[1]) # Obtains the port number

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(("127.0.0.1", port))
	server_socket.listen()

	clients = []
	create_file()

	while True:
		try: available = select.select([server_socket] + clients, [], [])[0]
		except ValueError:
			for client_socket in clients: # Checks for sockets that may have been closed
				if client_socket.fileno() == -1: clients.remove(client_socket) # Closed socket
			continue # Reiterates select

		for client_socket in available:
			if client_socket is server_socket: # New client
				newclient, addr = server_socket.accept()
				clients.append(newclient)
			else: # Existing client
				if len(client_socket.recv(1, socket.MSG_PEEK)) != 0: new_msg(client_socket) # Checks for client's message
				else: # Disconnection
					clients.remove(client_socket)
					clean_client(client_socket)
					client_socket.close()
					break # Reiterates select


if __name__ == "__main__":
	main(sys.argv)
