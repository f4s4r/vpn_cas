import socket
import threading
import os
import hashlib
from tun import create_tun
from crypto import encrypt, decrypt

server_host = "vpnserver"
server_port = 1194

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

action = input("register or login? ").strip().upper()
username = input("username: ")
password = input("password: ")
password_hash = hashlib.sha256(password.encode()).hexdigest()

message = action + "|" + username + "|" + password_hash
sock.sendto(message.encode(), (server_host, server_port))

reply, addr = sock.recvfrom(2048)

if reply == b"OK":
    print("auth ok, starting tunnel")

    tun = create_tun("tun0", "10.0.0.2")
    print("tunnel is up")

    def tun_to_udp():
        while True:
            packet = os.read(tun, 2048)
            sock.sendto(encrypt(packet), (server_host, server_port))

    def udp_to_tun():
        while True:
            data, a = sock.recvfrom(4096)
            os.write(tun, decrypt(data))

    t1 = threading.Thread(target=tun_to_udp)
    t2 = threading.Thread(target=udp_to_tun)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
else:
    print("auth failed")
