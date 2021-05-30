import random

def generate(signs : str, length : int):
    return ''.join([random.choice(signs) for x in range(length)])

def encode(message : str):
    return message.encode()

def decode(message):
    return message.decode()