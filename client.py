# from email import message
import socket
import threading
import time
import sys
import subprocess
import signal
import re
from retrieve import *
# from image import *
import os
import tqdm
# import tkinter
# import tkinter.scrolledtext
# from tkinter import simpledialog

def handler(signum, frame):
    print(username+"is disconnected")
    client.close()
    exit(1)

signal.signal(signal.SIGINT, handler)

import rsa
from encrypt import RSA
import re

client_mas = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_mas.connect(('localhost', 8082))
client_mas.send('need_min_port'.encode('ascii'))
free_port=int(client_mas.recv(1024).decode('ascii'))
client_mas.close()
print(free_port)
print(f"Connected with {str(free_port)}")
port = free_port
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', port))
# user = input("Type 'e' for existing user and 'n' for new user: ")
username =""


def recieve():
    filename = user +"_pri.pem"
    private_key = retrieve_private(filename)
    # print(5)
    while True:
        # print(6)
        try:
            try:
                msg =client.recv(128)
            except:
                msg = client.recv(1024)
            try:
                message = rsa.decrypt(msg, private_key).decode('ascii')

                print(message)
            except:
                    
                    k=msg.decode('ascii')

                    if(k=="*DOCS*"):
                        docnotif=client.recv(1024).decode('ascii')
                        print(docnotif)
                        docsize = docnotif.split(",size(KB): ")[1]
                        tmp=docnotif.split(",size(KB): ")[0]
                        lst=tmp.split(" ")
                        ofilename = "new_"+lst[-1]
                        with open(ofilename, "wb") as ofile:
                            data = client.recv(128)
                            
                            # ofile.write(ofile_bytes)
                            while data:
                                print(data)
                                ofile_bytes=rsa.decrypt(data, private_key)
                                ofile.write(ofile_bytes)
                                data = client.recv(128)
                        print("recieved "+ofilename+" from "+lst[0])    
                    else:
                        print(k)
                    if k == "":
                        print("overflow")
                        break   
                    print(15)
                    


        except:
            # print(10)
            print("An error occured")
            client.close()
            break

def write():
    while True:

        print("Type 0 for Group chat, 1 for Personal")
        chat_type = input("")
        client.send(chat_type.encode('ascii'))

        if int(chat_type) == 0:
            while True:
                print('Enter NEW to create a group / Enter VIEW to view groups / Enter BACK to exit groups ')
                choice = input("")
                client.send(choice.encode('ascii'))
                if choice.strip()=="NEW":
                    msg = client.recv(1024).decode('ascii')
                    # print(msg)
                    text=input(msg)
                    
                    client.send(text.encode('ascii'))
                    msg1=client.recv(1024).decode('ascii')
                    
                    print(msg1)

                

                elif choice.strip()=="VIEW":
                    gp_data = (client.recv(1024).decode('ascii'))
                   
                    gps =eval(gp_data)
                    # print(23134)
                    print(gps)
                    grp_choice = input("Connect to (grp): ")
                    client.send(grp_choice.encode('ascii'))
                    while(True):
                        tmp = (client.recv(1024).decode('ascii'))
                        choice1 = input(tmp)
                        client.send(choice1.encode('ascii'))
                        if choice1 == "ADD":
                            client.send(input("USERNAME: ").encode('ascii'))
                        if choice1 == "MESSAGE":
                            msg = input(">>>") 
                            # print(st)
                            msg=grp_choice+"::"+username+": "+msg
                            client.send(msg.encode('ascii'))
                        if choice1 == "KICK":
                            client.send(input("USERNAME: ").encode('ascii'))
                        if choice1 == "BACK":
                            break
                elif choice.strip() == "BACK":
                         break
                # group_name = input("")
                # client.send(group_name.encode('ascii'))

        if int(chat_type) == 1:
            
            send_to_name=input("Connect to: ").strip()
            print(23)
            client.send(send_to_name.encode('ascii'))
            print(34)
            s=client.recv(322)
            print(s)
            k =s.decode('ascii')
            t=eval(k)
        
            print(2)
            print(t)
            public_partner = rsa.PublicKey(n=int(t[0]), e=int(t[1]))
            print(3)
            while True:
                mess_type = input(">>>")

                if(mess_type == "*DOCS*"):
                    client.send(mess_type.encode('ascii'))
                    filename=input("input file name: ")
                    
                    file_size = os.path.getsize(filename)
                    sz = username+" sent "+filename+",size(KB): "+str(file_size)+""
                    client.send(sz.encode('ascii'))
                    with open(filename,"rb") as file:
                        data = file.read(117)
                        
                        while data:
                            l =rsa.encrypt(data, public_partner)
                            print(len(l))
                            client.send(l)
                            data = file.read(117)
                            
                    # client.send(mess_type.encode('ascii'))
                    # break
                elif(mess_type == "*BACK*"):
                    client.send(mess_type.encode('ascii'))
                    break
                elif(mess_type != ""):
                    message = f'{username}: {mess_type}'
                    client.send(rsa.encrypt(message.encode(), public_partner))
                    
                    # st=client.recv(1024).decode('ascii')
                    # print(st)
                    secs = time.time()
                    loc_time = time.ctime(secs)
                    # client.send(loc_time.encode('ascii'))



while True:

    print("Enter n if new user, e if existing user")
    
    
    choice = input("")
    client.send(choice.encode('ascii'))
    
    if(choice == "n") :
        print("--------------CREATE AN ACCOUNT-----------------")
        r1 = RSA()
        public_key = r1.public_key
        usr = client.recv(1024).decode('ascii')

        user = input(usr).strip()
        client.send(user.encode('ascii'))
        pwd = client.recv(1024).decode('ascii')
        pass1 =input(pwd)
        
        client.send(rsa.encrypt(pass1.encode(), public_key))
        con_pwd = client.recv(1024).decode('ascii')
        pass2  = input(con_pwd)
        if( pass1 == pass2):
            client.send("True".encode('ascii')) 
            subprocess.run(["/bin/bash", "private.sh", user])
            filename_pub = user+"_pub.pem"
            filename_pri = user+"_pri.pem"
            with open(filename_pri,"wb") as f:
                f.write(r1.private_key.save_pkcs1("PEM"))
            with open(filename_pub,"wb") as f:
                f.write(r1.public_key.save_pkcs1("PEM"))
        else:
            client.send("False".encode('ascii'))
        
        client.send(r1.public_key.save_pkcs1("PEM"))
        msg = client.recv(1024).decode('ascii')
        
        if msg.strip() == "SIGN UP SUCCESFULL!":
            username = user
            print(msg)
            print('Connected to server!')
            break
        else:
            print(msg)

    elif(choice == "e"):
        print("--------------LOG IN TO YOUR ACCOUNT-------------")
        usr = client.recv(1024).decode('ascii')
        user = input(usr).strip()
        client.send(user.encode('ascii'))

        pwd = client.recv(1024).decode('ascii')
        pass1 =input(pwd)
        filename = user +"_pub.pem"
        public_key = retrieve_public(filename)
        client.send(rsa.encrypt(pass1.encode('ascii'), public_key))
        filename = user +"_pri.pem"
        private_key = retrieve_private(filename)
        pass_db = rsa.decrypt(client.recv(1024), private_key).decode('ascii')
        if pass_db == pass1 :
            client.send("success".encode('ascii'))
            print('Connected to server!')
            username = user
            break
        else:
            client.send("fail".encode('ascii'))
            print("LOGIN FAILED")


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()