import socket
import psycopg2
from group import *
import os
import threading
from tkinter import *
from tkinter import filedialog
import sys
from unicodedata import name
from datetime import datetime
import rsa
from user import *
from login import *
from database import *

# port1 = int(sys.argv[1]) 

host = "localhost"
port = int(sys.argv[1]) 
# clients_list = []
# port = ports[g]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
server_mas = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_mas.connect(('localhost',8082))
server_mas.send(str(port).encode('ascii'))

names = [] 

# server.connect(('localhost',7052))
    
def handle1():
    print("55555555555555555555555555555")
    while True:
       for client_obj in clients_list:
            unread(client_obj)
            unread_grp(client_obj)
def unread(client_obj):
    client = client_obj.client
    # unread_table = "SELECT FROM_USER,MESSAGE,TIME_STAMP FROM MESSAGES WHERE TO_USER = %s"
    unread_table = "SELECT MESSAGE FROM MESSAGES WHERE TO_USER = %s"
    name = (client_obj.name,)
    mycursor.execute(unread_table,name)
    unread_msgs = mycursor.fetchall()
    if(unread_msgs):
        for row in unread_msgs:
            print(row[0])
            query2 = "DELETE FROM MESSAGES WHERE TO_USER = %s"
            val2 = (client_obj.name,)
            mycursor.execute(query2,val2)
            mydb.commit()
            # client.send("@#!").encode('ascii')
            # rc = client.recv(1024).decode('ascii')
            if(1==1):
                print("sadf")
                broadcast(row[0],client_obj.name,"lokesh","abnaja")
            else:
                print("lll")
            
            
            # time.sleep(2)
            
            
    else:
        return

def unread_grp(client_obj):
    client = client_obj.client
    unread_msgs = "SELECT MESSAGE,GROUP_NAME,UNSEEN_BY,ID FROM GROUP_MESSAGES WHERE UNSEEN_BY like %s"
    to_name = "%'"+client_obj.name + "'%"
    val =(to_name,)
    mycursor.execute(unread_msgs,val)
    grps_msgs = mycursor.fetchall()
    # print(23133)
    if(grps_msgs):
       
        for row in grps_msgs:
            unsent = eval(row[2])
            
            unsent.remove(client_obj.name)
            
            if len(unsent)!=0:
                print(100)
                query1 = "UPDATE GROUPS SET UNSEEN_BY = %s WHERE id = %s"
                val1 = (str(unsent),row[3])
                mycursor.execute(query1,val1)
                mydb.commit()
                print(11)
            else :
                print("delete")
                try :
                    query2 = "DELETE FROM GROUP_MESSAGES WHERE id = %s"
                    val2 = (row[3],)
                    mycursor.execute(query2,val2)
                    mydb.commit()
                except:
                    print("couldnt delete")  
                print(233)
            broadcast(row[0],client_obj.name,"lokesh","abnaja")

    
    

def retrive_token(user):
    val = (user,)
    state = "SELECT public_key FROM USERDATA WHERE username = %s "
    
    mycursor.execute(state,val)
    pass_db = mycursor.fetchall()
    
    for row in pass_db:
        # print(row[0])
        client.send(row[1])

def broadcast(message,name,sender,time):
    print(message)
    sent = False
    print(89)
    print(clients_list)
    print(name)
    for client_obj in clients_list:
        if client_obj.name == name :
            print(1234)
            print(message)
            client_obj.client.send(message)
            print(25167)
            # client_obj.client.recv(1024).decode('ascii')
            # print(message)
            sent = True
    # if not sent:
    #     usr="@chk:"+name
    #     print(usr)
    #     server_mas.send(usr.encode('ascii'))
    #     rcvr_stat=server_mas.recv(1024).decode('ascii')
    #     print(rcvr_stat)
    #     if rcvr_stat=="online":
    #         print(message)
    #         print(212567555)
    #         server_mas.send(message)
    #         print(2312122)

    state = "SELECT * FROM USERDATA WHERE USERNAME = %s"
    user = (name,)
    mycursor.execute(state,user)
    

    if mycursor.fetchall():
        # print(message)
        query = 'INSERT INTO MESSAGES (FROM_USER,TO_USER,MESSAGE,TIME_STAMP,STATUS) VALUES (%s,%s,%s,%s,%s)'  
        
        stat = str(sent)
        val = (sender,name,message,time,stat,)
        print(4)
        if stat == "False":
            print(6)
            try:
                print(len(message))
                mycursor.execute(query,val)
                print(5)
                print(message)
                mydb.commit()
            except:
                print("Can't insert into DB")
    else:
        print(7)
        for client_obj in clients_list:
            if client_obj.name == sender :
                message1 ="USER DOESNT EXIST!"
                client_obj.client.send(message1.encode('ascii'))

def handle(client_obj):
    
    client = client_obj.client
    sender = client_obj.name
    while True:
        
        try:
            print(clients_list)
            chattype = client.recv(1024).decode('ascii')
            if int(chattype) == 0:
                unread_grp(client_obj)
                
                while(True):

                    recieved_choice = client.recv(1024).decode('ascii')
                            
                    if( recieved_choice.strip()== "NEW"):
                        name ="PLS ENTER GRP NAME: "
                        client.send(name.encode('ascii'))
                        gp_name = client.recv(1024).decode('ascii')
                        print(111)
                        if gp_name!="":
                            G1 = Group(gp_name,client_obj)
                            print(222)
                            msg = gp_name+" is created succesfully"
                            client.send(msg.encode('ascii'))


                    elif(recieved_choice.strip()=="VIEW"):
                        
                            client.send(str(client_obj.in_groups).encode('ascii'))
                            grp = client.recv(1024).decode('ascii')
                            count=0
                            for group_obj in groups:
                                if group_obj.name == grp:
                                    count = count+1
                                    while(True):
                                        group_obj.options(client_obj)
                                        choice = client.recv(1024).decode('ascii')
                                        if choice.strip()=="ADD":
                                            person = client.recv(1024).decode('ascii')
                                            state = "SELECT username FROM USERDATA WHERE username = %s"
                                            val =(person,)
                                            mycursor.execute(state,val)
                                            print(10)
                                            if mycursor.fetchall():
                                                print(40)
                                                group_obj.add(person,client_obj)
                                            mydb.commit()
                                        
                                        elif choice.strip() == "MESSAGE":
                                            msg = client.recv(1024).decode('ascii')
                                            group_obj.broadcast_to_group(msg,client_obj.name)
                                        elif choice.strip() == "KICK":
                                            person = client.recv(1024).decode('ascii')
                                            state = "SELECT username FROM USERDATA WHERE username = %s"
                                            val =(person,)
                                            mycursor.execute(state,val)
                                            if mycursor.fetchall():
                                                print(40)
                                                group_obj.kick(person,client_obj)
                                            mydb.commit()

                                        elif choice.strip() == "BACK":
                                            break
                                if count == 1:
                                    break
                        # except:
                        #         if client_obj in clients_list:
                        #             clients_list.remove(client_obj)
                        #             client_obj.client.close()
                        #             print(client_obj.name +" is disconnected")
                        #         break
                                    
                    elif(recieved_choice.strip()=="BACK"):
                        break
                    elif(recieved_choice.strip()== ""):
                        if client_obj in clients_list:
                            clients_list.remove(client_obj)
                            client_obj.client.close()
                            print(client_obj.name +" is disconnected")
                            break
            
                    # print(groups)
        
            elif int(chattype) ==1:
                unread(client_obj)
               
                recv_name=client.recv(1024).decode('ascii')
                if(recv_name==""):
                    if client_obj in clients_list:
                        clients_list.remove(client_obj)
                        client_obj.client.close()
                        print(client_obj.name +" is disconnected")
                    break
                state = "SELECT public_key_n,public_key_e FROM USERDATA WHERE USERNAME = %s"
                user = (recv_name,)
                mycursor.execute(state,user)
                # mycursor.execute(state,val)
                pass_db = mycursor.fetchall()
                for row in pass_db:
                    print(row)
                    client.send(str(row).encode('ascii'))
                    print(56)
                    
                while True:
                    message = client.recv(128)
                    
                    if(message == b''):
                        print(892019209)
                        break
                   
                    

                    print(22)
                    try:
                        msg=message.decode('ascii')
                        if msg == "*BACK*":
                            break
                        else:
                            loc_time="time"
                            # if msg!="*DOCS*":
                            broadcast(msg,recv_name,sender,loc_time)
                            print(23456)
                        # if msg == "*DOCS*":
                        #     loc_time="time"
                        #     broadcast(msg,recv_name,sender,loc_time)
                        #     fsize=client.recv(1024).decode('ascii')
                        #     client.send(fsize.encode('ascii'))
                        #     data=client.recv(int(fsize))
                        #     client.sendall(data)
                            
                    except:
                        # print(23456)
                        # client.send("sent".encode('ascii'))
                        
                        loc_time = "time"
                        # print(123)
                        # print(message)
                        broadcast(message,recv_name,sender,loc_time)
                        # client.re
        except:
            if client_obj in clients_list:
                clients_list.remove(client_obj)
                client_obj.client.close()
                msg=client_obj.name +" is disconnected"
                print(msg)
                msg="@rem:"+client_obj.name
                server_mas.send(msg.encode('ascii'))

            break

def recieve():
    while True:
        
        client,addr = server.accept()
        # client.send()
        
        #print(addr)
        
        #client.send('NICK'.encode('ascii'))
        
        while True:
            
            choice= client.recv(1024).decode('ascii')
            # print("111")
            # user = client.recv(1024).decode('ascii')
            if( choice =="n"):
                client_obj = sign_up(client,port)
                if client_obj != -1:
                    print(90)
                    msg="@usr:"+client_obj.name
                    server_mas.send(msg.encode('ascii'))
                    break
                
            
            if( choice == "e"):
                client_obj = sign_in(client,port)
                # client_obj.in_groups
                if client_obj != -1:
                    msg="@usr:"+client_obj.name
                    server_mas.send(msg.encode('ascii'))
                    break
        print(F"Connected with {str(addr)}")
        print(clients_list)
        clients_list.append(client_obj)
        print(f'Name of client is {client_obj.name}')

        # client.send('Connected to server!'.encode('ascii'))
        # thread = threading.Thread(target = ser_con, args=(server))
        
        
        thread = threading.Thread(target = handle, args=(client_obj,))
        thread.start()
        

        # thread = threading.Thread()

thread1 = threading.Thread(target = handle1, args=())
thread1.start()       
recieve()
