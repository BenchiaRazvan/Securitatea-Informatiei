from ctypes import c_char
import socket
import os
import random
from threading import Thread
from Crypto.Cipher import AES
import secrets
import pickle

s = socket.socket()

def randomBytes(n):
    return bytearray(random.getrandbits(8) for i in range(n))

def generateRandomKey():

    key = b""
    key += randomBytes(16)

    return key


globalKey = generateRandomKey()

def encryptKey(key1, key2):
    
    mode = AES.MODE_ECB

    encryptor = AES.new(key2, mode)

    ciphertext = encryptor.encrypt(key1)

    f = open("bytes.txt", "wb")
    f.write(ciphertext)
    f.close()

def decriptKey():

    file = open("bytes.txt", "rb")
    text = file.readline()
    decipher = AES.new(globalKey, AES.MODE_ECB)
    decriptText = decipher.decrypt(text)

    return decriptText
    
    
def AesCFBEncrypt(IV, key):

    file = open("plaintext.txt", "r")
    pt = int(file.readline())

    mode = AES.MODE_ECB
    encryptor = AES.new(key, mode)
    
    ciphertext = encryptor.encrypt(str(IV).encode('utf-8'))
     

    val_cyphertext = int.from_bytes(ciphertext, "big")
    val_cyphertext = bin(val_cyphertext)[2:]

    val_plaintext = bin(pt)[2:]

    multiplu = 128
    while(multiplu < len(val_plaintext)):
        multiplu = multiplu + 128
    
    difference = multiplu - len(val_plaintext)
    
    for x in range(difference):
        val_plaintext = val_plaintext + "0"
    

    blocks = len(val_plaintext) / 128
    a_list = [None] * len(val_plaintext)

    i = 1
    j = 128
    while(blocks != 0):
        for i in range(j):
            a_list[i] = int(val_cyphertext[i]) ^ int(val_plaintext[i])                      
        i = j
        j = j + 128
        blocks -= 1
        
    f = open("CFB.txt", "wb")
    f.write(ciphertext)
    f.close()



def AesECBEncrypt(key):

    file = open("plaintext.txt", "r")
    plainText = int(file.readline())
    bin_plaintext = bin(plainText)[2:]

    multiplu = 128

    while(multiplu < len(bin_plaintext)):
        multiplu = multiplu + 128
  
    difference = multiplu - len(bin_plaintext)

    for x in range(difference):
       bin_plaintext = bin_plaintext + "0"

    blocks = len(bin_plaintext) / 128
    
    a_list = [None] * len(bin_plaintext)

    i = 128

    while(blocks != 0):
        
        a_list = bin_plaintext[:i]
        mode = AES.MODE_ECB
        encryptor = AES.new(key, mode)
        ciphertext = encryptor.encrypt(str(a_list).encode('utf-8'))
        i = i + 128
        blocks -= 1

    f = open("ECB.txt", "wb")
    f.write(ciphertext)
    f.close()


def listener(client, address):
    print ("Accepted connection from: ", address)

    while True:
        data = client.recv(1024)
        if not data:
            break
        else:
            if(str(data).__contains__('ecb')):
                encryptKey(generateRandomKey(), globalKey)
                decriptKey()
                AesECBEncrypt(decriptKey())
                client.sendall(globalKey)
                #print("Cheia decriptata:" + str(decriptKey()))
            else:
                encryptKey(generateRandomKey(), globalKey)
                decriptKey()
                AesCFBEncrypt('0' * 128, decriptKey())
                client.sendall(decriptKey())
            
    client.close()

host = 'localhost'
port = 10015


s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(3)
th = []

while True:
    print ("Server is listening for connections...")
    client, address = s.accept()
    th.append(Thread(target=listener, args = (client,address)).start())
