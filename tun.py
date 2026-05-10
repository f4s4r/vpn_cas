import os
import fcntl
import struct
import subprocess

TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000

def create_tun(name, ip):
    tun = os.open("/dev/net/tun", os.O_RDWR)
    ifr = struct.pack("16sH", name.encode(), IFF_TUN | IFF_NO_PI)
    fcntl.ioctl(tun, TUNSETIFF, ifr)
    subprocess.run(["ip", "addr", "add", ip + "/24", "dev", name])
    subprocess.run(["ip", "link", "set", name, "up"])
    return tun
