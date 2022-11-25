import os

def send_img(filename):
    f = open(filename, "rb")
    l = os.path.getsize(filename)
    m = f.read(l)
    f.close()
    return m

def recieve_img(filename,client):

    f = open(filename, "wb")
    data = None
    while True:
        m = client.recv(1024)
        data = m
        if m:
            while m:
                m = client.recv(1024)
                data+=m
            else:
                break
    f.write(data)
    f.close()