from cryptography.fernet import Fernet

def encoder(data):
    try:
        return data.encode('utf-8')
    except:
        return data

def decoder(data):
    try:
        return data.decode('utf-8')
    except:
        return data

def keygen():
    return Fernet.generate_key()

def encrypt(data, key):
    try:
        return encoder(Fernet(encoder(key)).encrypt(encoder(data)))
    except:
        return ''

def decrypt(data, key):
    try:
        return decoder(Fernet(encoder(key)).decrypt(encoder(data)))
    except:
        return ''