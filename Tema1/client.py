from ctypes import c_char
import socket
import os
import random
from threading import Thread
from Crypto.Cipher import AES
import secrets
import pickle


s = socket.socket()
port = 10015
s.connect(('localhost', port))


while(1):

    num = input ("Tasteaza modul in care doresti criptarea mesajelor: ")
    s.send(num.encode())
    data = s.recv(1000000)
    
    def decriptKey(key):

        file = open("bytes.txt", "rb")
        text = file.readline()
        decipher = AES.new(key, AES.MODE_ECB)
        decriptText = decipher.decrypt(text)

        return decriptText

    #print("Cheia decriptata este: " + str(decriptKey(data)))
