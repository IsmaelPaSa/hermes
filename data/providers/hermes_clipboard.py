import pyperclip3 as clipboard

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

def get():
    try:
        return decoder(clipboard.paste())
    except:
        return ''

def set(text):
    try:
        print(decoder(text))
        clipboard.copy(decoder(text))
    except:
        return False
    return True