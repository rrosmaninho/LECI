# test_client.py

import pytest
from subprocess import PIPE
from subprocess import Popen 

def test_main():
    print("Testa o comportamento de main")

    proc = Popen("python3 client.py", stdout=PIPE, shell=True) 
    output = proc.stdout.read().decode("utf-8") 
    assert output == "Usage: python3 client.py client_id socket [address]\n"

    proc = Popen("python3 client.py Ru2i 1234", stdout=PIPE, shell=True) 
    output = proc.stdout.read().decode("utf-8") 
    assert output == "Client_id must not be empty or can only have alphabetical characters!\n"

    proc = Popen("python3 client.py 113553 1234", stdout=PIPE, shell=True) 
    output = proc.stdout.read().decode("utf-8") 
    assert output == "Client_id must not be empty or can only have alphabetical characters!\n"

    proc = Popen("python3 client.py 1234 127.0.0.1", stdout=PIPE, shell=True) 
    output = proc.stdout.read().decode("utf-8") 
    assert output == "Client_id must not be empty or can only have alphabetical characters!\n"

    proc = Popen("python3 client.py Rui 127.0.0.1", stdout=PIPE, shell=True) 
    output = proc.stdout.read().decode("utf-8") 
    assert output == "Socket must not be empty or can only be positive integer!\n"

    proc = Popen("python3 client.py Rui -1234", stdout=PIPE, shell=True) 
    output = proc.stdout.read().decode("utf-8") 
    assert output == "Socket must not be empty or can only be positive integer!\n"