import socket

RECEIVER_ADDR = ('127.0.0.1', 10001)
SENDER_ADDR = ('127.0.0.2', 10002)
PROXY_ADDR = ('127.0.0.3', 10003)
SECOND_RECEIVER_ADDR = ('127.0.0.4', 10004)


def sender():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(SENDER_ADDR)

        for i in range(1000):
            sock.sendto(bytes('Hello_' + str(i), 'ascii'), PROXY_ADDR)

        sock.sendto(bytes("EOF-EOF-EOF-EOF-EOF", 'ascii'), PROXY_ADDR)

    except Exception as ex:
        print(ex)
    finally:
        sock.close()


if __name__ == '__main__':
    sender()