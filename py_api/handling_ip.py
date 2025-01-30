import socket
import os

def ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def save_ip(ip):
    if os.path.exists("../ip.txt"):
        os.remove("../ip.txt")

    with open("../ip.txt", 'w') as file:
        file.write(ip)