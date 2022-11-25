import rsa
def retrieve_private(filename):
    with open(filename, mode='rb') as file:
        key_data = file.read()
        private_key = rsa.PrivateKey.load_pkcs1(key_data)
        return private_key

def retrieve_public(filename):
    with open(filename, mode='rb') as file:
        key_data = file.read()
        public_key = rsa.PublicKey.load_pkcs1(key_data)
        return public_key