from database import *
clients_list = []
print(clients_list)
class Client:
    in_groups=[]
    
    def __init__(self,username,client):
        
        self.client = client
        self.name = username     # default username and password
        self.in_groups=[]
        query = "SELECT GROUP_NAME FROM GROUPS WHERE GROUP_MEMBERS like %s "
        db_name = "%'"+self.name + "'%"
        val =(db_name,)
        mycursor.execute(query,val)
        grps = mycursor.fetchall()
        if(grps):
            for row in grps:
                print(row)
                if row[0] not in self.in_groups:
                    self.in_groups.append(row[0])
        mydb.commit()
    # def added_to_grp(self,grp_obj): 
    #     query = "SELECT GROUP_NAME FROM GROUPS WHERE GROUP_MEMBERS like %s "
    #     db_name = "%'"+self.name + "'%"
    #     val =(db_name,)
    #     mycursor.execute(query,val)
    #     grps = mycursor.fetchall()
    #     if(grps):
    #         for row in grps:
    #             if row[0] not in self.in_groups:
    #                 self.in_groups.append(row[0])
                    
            
    
def check_name_in_list(name,liststr):
    namelist = eval(liststr)
    if name in namelist:
        return True
    else:
        return False
