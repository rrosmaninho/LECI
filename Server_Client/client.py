#!/usr/bin/python3

import os
import sys
import json
import socket
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from common_comm import send_dict, recv_dict, sendrecv_dict

# Returns int data encrypted in a 16 bytes binary string and coded base64
def encrypt_intvalue(cipherkey, data):
	return str(base64.b64encode(cipherkey.encrypt(bytes("%16d" %(data), "utf8"))), "utf8")


# Returns int data decrypted from a 16 bytes binary string and coded base64
def decrypt_intvalue(cipherkey, data):
	return int(str(cipherkey.decrypt(base64.b64decode(data)), "utf8"))


# Validates server's response, exits if error
def validate_response(client_socket, response):
	if not response["status"]:
		print(response["error"])
		client_socket.close()
		sys.exit(3)


# Support for the client's withdrawal
def quit_action(client_socket):
	validate_response(client_socket, sendrecv_dict(client_socket, {'op': 'QUIT'}))
	print("User withdrawal successful")
	client_socket.close()
	sys.exit(4)


# Suport for executing the client pretended behaviour
def run_client(client_socket, client_id):
	userInput = (input("(YES/NO) Use cipher? ")).upper() # Asks client for cipher usage preference
	if userInput == "YES":
		useChiper = True
		cipherkey = os.urandom(16)
		cipherkey_tosend = str(base64.b64encode(cipherkey), "utf8")
		cipher = AES.new(cipherkey, AES.MODE_ECB)
		request = { "op": 'START', "client_id" : client_id , "cipher": cipherkey_tosend }
	elif userInput == "NO": 
		useChiper = False
		request = { "op": 'START', "client_id" : client_id , "cipher": None }
	else:
		print("Answer must be 'YES' or 'NO'")
		sys.exit(3) 
	validate_response(client_socket, sendrecv_dict(client_socket, request)) # Validates response using function validate_response *after* automatic START

	numbers = [] # List to store numbers sent to the server
	while True: # Enters a loop until withdrawal or 'STOP' input operation
		userInput = input("Number: ") # Asks the client for a number
		if not userInput.lstrip("-").isdigit(): # Ignores negative sign
			if userInput.upper() == 'STOP': break # Checks for client's wish to stop
			if userInput.upper() == 'QUIT': quit_action(client_socket) # Checks for withdrawal and uses function quit_action
			sys.exit(3)
		numbers.append(userInput) # Adds client's input number to the numbers list
		if useChiper: request = { "op": 'NUMBER', "number": encrypt_intvalue(cipher, int(userInput)) } # Checks if client's cipher usage preference (Ciphering function used)
		elif not useChiper: request = { "op": 'NUMBER', "number": int(userInput) } # Checks if client's cipher usage preference (No cipher usage)
		validate_response(client_socket, sendrecv_dict(client_socket, request)) # Validates response using function validate_response *after* request
	response = sendrecv_dict(client_socket, { "op": 'STOP'} ) # Automatic STOP
	validate_response(client_socket, response) # Validates response using function validate_response
	if useChiper: print("Numbers given: {}\nNumber chosen: {}".format(numbers, decrypt_intvalue(cipher, response["value"]))) # Checks if client's cipher usage preference (Deciphering function used)
	elif not useChiper: print("Numbers given: {}\nNumber chosen: {}".format(numbers, response["value"])) # Checks if client's cipher usage preference (No decipher usage)

	userInput = input("Guess: ").lower() # Asks for client's guess
	if userInput == 'quit': quit_action(client_socket) # Checks for withdrawal
	elif userInput not in ["min", "max", "first", "last", "median"]: sys.exit(3) # Checks if input was outside of possible solutions
	response = sendrecv_dict(client_socket, { "op": 'GUESS', "choice": userInput }) # Automatic GUESS
	validate_response(client_socket, response) # Validates response using function validate_response
	print(response["result"]) # Prints result (TRUE or FALSE)


def main(argvs):
	if not 3 <= len(argvs) <= 4: # Validates the number of arguments, prints error message and exits with error
		print("Usage: python3 client.py client_id socket [address]")
		sys.exit(1)
	elif not argvs[1].isalpha(): # Validates the client's ID argument, prints error message and exits with error
		print("Client_id must not be empty or can only have alphabetical characters!")
		sys.exit(2)
	elif not (argvs[2].isdigit() and int(argvs[2]) >= 0): # Validates the port argument, prints error message and exits with error
		print("Socket must not be empty or can only be positive integer!")
		sys.exit(2)

	port = int(argvs[2]) # Obtains the port number

	# Obtains the hostname (localhost or another host)
	if len(argvs) == 4 and all([0<=int(number)<=255 for number in argvs[3].split(".")]): # Validates the client's [address] argument
		print("Valid hostname! Hostname set as {}!".format(argvs[3])) 
		hostname = argvs[3] 
	else: # Default [address] if the client's input is not valid
		print("Invalid hostname! Hostname set as default value!") 
		hostname = "127.0.0.1" 

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.bind(("0.0.0.0", 0))
	client_socket.connect((hostname, port))

	run_client(client_socket, sys.argv[1])
	
	client_socket.close()
	sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
