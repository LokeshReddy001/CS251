import rsa

class RSA:
    def __init__(self):
        self.public_key, self.private_key = rsa.newkeys(1024)
        
