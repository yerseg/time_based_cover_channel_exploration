import os

os.sys.path.append('/home/yerseg/.local/lib/')

from scapy.all import *

RECEIVER_ADDR = ('127.0.0.1', 10001)
SENDER_ADDR = ('127.0.0.100', 10002)
PROXY_ADDR = ('127.0.0.10', 10003)
SECOND_RECEIVER_ADDR = ('127.0.0.150', 10005)

dup = False

sent = False
index = 0
MESSAGE = "#COVERT MESSAGE!#"

def generate_ttl(original_ttl):
    global index

    if index != len(MESSAGE):
        index += 1
        return ord(MESSAGE[index - 1])

    return original_ttl


def proxy():
    try:
        print(get_if_list())

        def callback(packet):
            global dup

            if dup is True:
                dup = False
                return

            dup = True

            new_ip_header = IPv6(src=packet['IPv6'].src, dst='::1', hlim=generate_ttl(packet['IPv6'].hlim))
            new_udp_header = UDP(sport=packet['UDP'].sport, dport=10005)
            new_packet = new_ip_header / new_udp_header / Raw(packet['UDP'].payload)
            del new_packet[IPv6].chksum
            del new_packet[UDP].chksum
            del new_packet[IPv6].payload.chksum

            send(new_packet)

        sniff(prn=callback, filter="src port 10002 and dst port 10001", iface='lo')

    except Exception as ex:
        print(ex)

    finally:
        pass


if __name__ == '__main__':
    proxy()