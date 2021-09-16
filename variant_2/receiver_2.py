import os

os.sys.path.append('/home/yerseg/.local/lib/')

from scapy.all import *

RECEIVER_ADDR = ('127.0.0.1', 10001)
SENDER_ADDR = ('127.0.0.100', 10002)
PROXY_ADDR = ('127.0.0.10', 10003)
SECOND_RECEIVER_ADDR = ('127.0.0.150', 10005)

message_begin = False

dup = False

def decode_and_print_covert_message(packet):
    global message_begin

    if (packet['IPv6'].hlim == ord('#')):
        if message_begin is False:
            message_begin = True
            return
        else:
            message_begin = False
            return

    if message_begin is True:
        print(chr(packet['IPv6'].hlim))

def is_eof(pkt):
    if bytes(pkt['Raw']).find(bytes('EOF-EOF-EOF-EOF-EOF', 'utf-8')) != -1:
        return True

    return False

def receiver():
    try:
        def callback(packet):
            global dup

            if dup is True:
                dup = False
                return

            dup = True

            decode_and_print_covert_message(packet)

            with open("./files/new_file_" + str(0) + ".pdf", 'ab') as file:
                file.write(bytes(packet['Raw']))

        sniff(prn=callback, filter="src port 10002 and dst port 10005",
            iface='lo', stop_filter=lambda x: is_eof(x))

    except Exception as ex:
        print(ex)
    finally:
        pass

if __name__ == '__main__':
    receiver()