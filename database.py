import psycopg2
try:
    mydb = psycopg2.connect(
    host='localhost',
    user='CS251',
    password='coolcoders',
    database = 'PROJECT',
    port = 5432
    )
    mycursor = mydb.cursor()
    
    
except:
    print("Can't connect to db")


mycursor.execute('''CREATE TABLE IF NOT EXISTS USERDATA
(USERNAME varchar(255) NOT NULL,
PASSWORD bytea NOT NULL,
LAST_LOGIN varchar(255) NOT NULL,
PUBLIC_KEY_N varchar(2000) NOT NULL,
PUBLIC_KEY_E varchar(500) NOT NULL)
''')

# print(222)
mycursor.execute('''CREATE TABLE IF NOT EXISTS MESSAGES
(ID serial PRIMARY KEY,
FROM_USER varchar(255) NOT NULL,
TO_USER varchar(255) NOT NULL,
MESSAGE bytea NOT NULL,
TIME_STAMP varchar(255) NOT NULL,
STATUS varchar(255) NOT NULL)
''')

mycursor.execute(''' CREATE TABLE IF NOT EXISTS GROUPS
(GROUP_NAME varchar(255) NOT NULL,
ADMIN_NAME varchar(255) NOT NULL,
GROUP_MEMBERS varchar(20000) NOT NULL)
''')

mycursor.execute('''CREATE TABLE IF NOT EXISTS GROUP_MESSAGES
(ID serial PRIMARY KEY,
GROUP_NAME varchar(255) NOT NULL,
FROM_USER varchar(255) NOT NULL,
MESSAGE bytea NOT NULL,
UNSEEN_BY varchar(2000) NOT NULL)
''')

mydb.commit()