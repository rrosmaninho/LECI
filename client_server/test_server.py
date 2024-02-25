# test_server.py

import pytest
from subprocess import PIPE
from subprocess import Popen 
from server import new_client, quit_client, number_client, find_client_id, stop_client, guess_client

socket1 = "<socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 1234), raddr=('127.0.0.1', 49791)>"
socket2 = "<socket.socket fd=6, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 1234), raddr=('127.0.0.1', 50022)>"
socket3 = "<socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 1234), raddr=('127.0.0.1', 50047)>"

def test_main():
    print("Testa o comportamento de main")

    proc = Popen("python3 server.py", stdout=PIPE, shell=True) 
    output = proc.stdout.read().decode("utf-8") 
    assert output == "Usage: python3 server.py socket\n"

    proc = Popen("python3 server.py -1234", stdout=PIPE, shell=True) 
    output = proc.stdout.read().decode("utf-8") 
    assert output == "Socket must be a positive integer!\n"
    
def test_new_client():
    print("Testa o comportamento de new_client") 
    assert new_client(socket1, {'op': 'START', 'client_id': 'Rui', 'cipher': None}) == {'op': 'START', 'status': True}
    assert new_client(socket2, {'op': 'START', 'client_id': 'Maria', 'cipher': None}) == {'op': 'START', 'status': True}
    assert new_client(socket1, {'op': 'START', 'client_id': 'Rui', 'cipher': None}) == { "op": "START", "status": False, "error": "Cliente existente" }

def test_find_client_id():
    print("Testa o comportamento de find_client_id") 
    assert find_client_id(socket1) == "Rui"
    assert find_client_id(socket2) == "Maria"
    assert find_client_id(socket3) == None

def test_quit_client():
    print("Testa o comportamento de quit_client") 
    assert quit_client(socket1, {'op': 'START'}) == { "op": "QUIT", "status": True }
    assert quit_client(socket1, {'op': 'START'}) == { "op": "QUIT", "status": False, "error": "Cliente inexistente" }
    assert quit_client(socket3, {'op': 'START'}) == { "op": "QUIT", "status": False, "error": "Cliente inexistente" }

def test_number_client():
    print("Testa o comportamento de number_client") 
    assert number_client(socket1, {'op': 'NUMBER', 'number': '1'}) == { "op": "NUMBER", "status": False, "error": "Cliente inexistente" }
    assert number_client(socket2, {'op': 'NUMBER', 'number': '1'}) == {'op': 'NUMBER', 'status': True}
    assert number_client(socket3, {'op': 'NUMBER', 'number': '1'}) == { "op": "NUMBER", "status": False, "error": "Cliente inexistente" }

def test_stop_client():
    print("Testa o comportamento de stop_client") 
    assert stop_client(socket1, {'op': 'STOP'}) == { "op": "STOP", "status": False, "error": "Cliente inexistente" }
    assert stop_client(socket2, {'op': 'STOP'}) == { "op": "STOP", "status": True, "value" : '1'}

def test_guess_client():
    print("Testa o comportamento de guess_client") 
    assert guess_client(socket1, { "op": 'GUESS', "choice": 'min' }) == { "op": "GUESS", "status": False, "error": "Cliente inexistente" }