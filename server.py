import socket
import threading
import os
import db
from tun import create_tun
from crypto import encrypt, decrypt

db.init_db()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 1194))

print("server started, waiting for client")

data, client_addr = sock.recvfrom(2048)
parts = data.decode().split("|")
action = parts[0]
username = parts[1]
password = parts[2]

success = False
if action == "REGISTER":
    db.register(username, password)
    success = True
    print("registered user", username)
if action == "LOGIN":
    success = db.login(username, password)
    print("login attempt", username, success)

if success:
    sock.sendto(b"OK", client_addr)

    tun = create_tun("tun0", "10.0.0.1")
    print("tunnel is up")

    def tun_to_udp():
        while True:
            packet = os.read(tun, 2048)
            sock.sendto(encrypt(packet), client_addr)

    def udp_to_tun():
        while True:
            data, addr = sock.recvfrom(4096)
            os.write(tun, decrypt(data))

    t1 = threading.Thread(target=tun_to_udp)
    t2 = threading.Thread(target=udp_to_tun)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
else:
    sock.sendto(b"FAIL", client_addr)
    print("auth failed")
