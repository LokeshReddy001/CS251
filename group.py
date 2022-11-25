from user import *
groups = []
class Group:

    grp_clients =[]
        
    def __init__(self,name,*args):
        if(len(args)==1):
            client_obj = args[0]
            self.admin = client_obj.name #can raise exception if u want to
            self.name = name
            print(self.grp_clients)
            self.grp_clients=[]
            self.grp_clients.append(client_obj.name)
            client_obj.in_groups.append(self.name)
            print(self.grp_clients)
            groups.append(self)
            query = "INSERT INTO GROUPS (GROUP_NAME,ADMIN_NAME,GROUP_MEMBERS) VALUES (%s,%s,%s)"
            val = (self.name,self.admin,str(self.grp_clients))
            mycursor.execute(query,val)
            mydb.commit()
        elif(len(args)>1):
            self.admin = args[0]
            self.name = name
            # print(type(args[1]))
            # print(args[1])
            self.grp_clients = eval(args[1])
            groups.append(self)
            

        
    def broadcast_to_group(self,message,name):
        # for x in clients_list:
        #     if x.name in self.grp_clients:
        #         x.client.send(message.encode('ascii'))
        msg=message.encode('ascii')
        dummy = self.grp_clients.copy()
        print(dummy)
        # while len(dummy)!=0:
        print(clients_list)
        for client_obj in clients_list:
            print(clients_list)
            if client_obj.name in self.grp_clients:
                print(client_obj.name)
                print(dummy)
                dummy.remove(client_obj.name)
                print(dummy)
                client_obj.client.send(msg)
                    
        
        query = 'INSERT INTO GROUP_MESSAGES (GROUP_NAME,FROM_USER,MESSAGE,UNSEEN_BY) VALUES (%s,%s,%s,%s)' 
        unseen = str(dummy)
        print(unseen)
        val = (self.name,name,msg,unseen,)
        if len(dummy) != 0:
            try:
                mycursor.execute(query,val)
                mydb.commit()
            except:
                print("Can't insert into TABLE GROUP_MESSAGES")


    def if_admin(self,client_obj):
        if client_obj.name == self.admin:
            return True
        else:
            return False

    def kick(self,name,member): 
        if(self.if_admin(member)):
        # self.members.remove(ID)
            message = str(name.strip()) +" has been removed from grp" +" by "+ str(member.name) #TO DO -> byadmin
            self.broadcast_to_group(message,member.name)
            if name in self.grp_clients: 
                self.grp_clients.remove(name)
                query = "SELECT GROUP_MEMBERS FROM GROUPS WHERE GROUP_NAME = %s"
                val = (self.name,)
                mycursor.execute(query,val)
                mydb.commit()
                members = mycursor.fetchall()
                gp_members=[]
                if members:
                    for row in members:
                        print(row[0])
                        gp_members = eval(row[0])
                        gp_members.remove(name)
                query1 = "UPDATE GROUPS SET GROUP_MEMBERS = %s WHERE GROUP_NAME = %s"
                val1 = (str(gp_members),self.name)
                mycursor.execute(query1,val1)
                update_client_obj(member.name)                
                mydb.commit()

            

    
        
    def add(self,client_name,member):
        if(self.if_admin(member)):
            print(90)
            self.grp_clients.append(client_name)
            # client_obj.added_to_grp(self)
            message = str(client_name.strip()) +" has been added to " +str(self.name) +" by "+ str(member.name)# TO DO -> byadmin
            self.broadcast_to_group(message,client_name)
            query = "SELECT GROUP_MEMBERS FROM GROUPS WHERE GROUP_NAME = %s"
            val = (self.name,)
            mycursor.execute(query,val)
            mydb.commit()
            members = mycursor.fetchall()
            gp_members=[]
            if members:
                for row in members:
                    print(row[0])
                    gp_members = eval(row[0])
                    gp_members.append(client_name)
            query1 = "UPDATE GROUPS SET GROUP_MEMBERS = %s WHERE GROUP_NAME = %s"
            val1 = (str(gp_members),self.name)
            mycursor.execute(query1,val1)
            update_client_obj(client_name)
            mydb.commit()


    def options(self,client_obj):
        if(self.if_admin(client_obj)):
            message = "SELECT ADD"+"/"+"KICK"+"/"+"MESSAGE"+"/"+"BACK : "
            client_obj.client.send(message.encode('ascii'))
        else:
            message = "SELECT EXIT"+"/"+"MESSAGE/BACK : "
            client_obj.client.send(message.encode('ascii'))

def construct_groups():
    query = "SELECT * FROM GROUPS"
    mycursor.execute(query)
    group_details = mycursor.fetchall()
    mydb.commit()
    if group_details:
        for row in group_details:
            admin_name = row[1]
            name = row[0]
            gp_members = row[2]
            gp = Group(name,admin_name,gp_members)
            groups.append(gp)

def update_client_obj(name):
        for obj in clients_list:
            if obj.name == name:
                query = "SELECT GROUP_NAME FROM GROUPS WHERE GROUP_MEMBERS like %s "
                db_name = "%'"+name+"'%"
                val =(db_name,)
                in_grp_details = mycursor.execute(query,val)
                in_grp_list = []
                if in_grp_details:
                    for row in in_grp_details:
                        in_grp_list.append(row[0])
                obj.in_groups = in_grp_list
                mydb.commit()