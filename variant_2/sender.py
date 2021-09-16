import socket

RECEIVER_ADDR = ('::1', 10001)
SENDER_ADDR = ('::1', 10002)
PROXY_ADDR = ('::1', 10003)
SECOND_RECEIVER_ADDR = ('::1', 10004)


def sender():
    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sock.bind(SENDER_ADDR)

        with open("./Lr1.pdf", 'rb') as file:
            buffer = file.read(1024)
            while buffer:
                sock.sendto(buffer, RECEIVER_ADDR)
                buffer = file.read(1024)
            sock.sendto(bytes("EOF-EOF-EOF-EOF-EOF", 'utf-8'), RECEIVER_ADDR)

    except Exception as ex:
        print(ex)
    finally:
        sock.close()


if __name__ == '__main__':
    sender()