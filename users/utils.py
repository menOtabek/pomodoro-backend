import random
import string

def generate_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def generate_key(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
