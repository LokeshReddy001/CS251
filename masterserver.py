import socket
import threading
import sys
from database import *
from group import *

port_master = 8082
masterserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
masterserver.bind(('localhost', port_master))
masterserver.listen()
servers =[]
construct_groups()
all_users=[]
class Server:
    def __init__(self,serv_sock,port_no):
        self.socket=serv_sock
        self.port=port_no
        self.users=[]
def handle(server):
    while True:
        try:
            rcv = server.socket.recv(1024).decode('ascii')
            print(29)
            print(rcv)
            if(rcv!=None):
                print(0)
            else:
                print(-1)
            if rcv[0:5]=="@usr:":
                print(35)
                server.users.append(rcv[5:])
                all_users.append(rcv[5:])
                print(rcv[5:]+" connected")
        
            elif rcv[0:5]=="@rem:":
                print(36)
                server.users.remove(rcv[5:])
                all_users.remove(rcv[5:])
                print(rcv[5:]+" left the chat")
        except:
            print(789)
            True
#             elif rcv[0:5]=="@chk:":
#                 print(46)
#                 rcvr=rcv[5:]
#                 if rcvr in all_users:
#                     server.socket.send("online".encode('ascii'))
#                     print(628)
#                     msg=server.socket.recv(128)
                    # print(msg)
        #             print(167)
        #             for x in servers:
        #                 print(rcvr)
        #                 print(x.users)
        #                 if rcvr in x.users:
        #                     print("sent to rcvr")
        #                     x.socket.send(msg)
                            
        #                     print("sentntnt")
        #                     # k=x.socket.recv(1024).decode('ascii')
        #                     # print(k)
        #                     x.socket.send(rcvr.encode('ascii'))
        #                     print("wfwhuwhuwuw")
        #                     break
        #         else:
        #             server.socket.send("offline".encode('ascii'))
        # except:
        #     print(890)
        #     True

def recieve_ser():
    while True:
        
        server_sock,addr = masterserver.accept()
        server_port=server_sock.recv(1024).decode('ascii')
        if server_port == "need_min_port":
            server_sock.send(str(free_server()).encode('ascii'))
            server_sock.close()
        else:
            a=Server(server_sock,int(server_port))
            servers.append(a)
            
            thread = threading.Thread(target = handle, args=(a,))
            thread.start()
        
def free_server():
    min_users = len(servers[0].users)
    min_port=servers[0].port
    for s in servers[1:]:
        if len(s.users) < min_users:
            min_port=s.port
    return min_port

recieve_ser()