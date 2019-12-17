from socket import *
import os

def sniffing(host):
    if os.name == 'nt':
        socket_protocol = IPPROTO_IP
    else:
        socket_protocol = IPPROTO_ICMP

    sniffer = socket(AF_INET, SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    sniffer.setsockopt(IPPROTO_IP, IP_HORINCL, 1)

    packet = sniffer.recvfrom(65565)
    print(packet)

print(gethostname())
host = gethostbyname(gethostname())
print('start sniffing {0}'.format(host))
sniffing('172.17.196.178')
