import socket

RECEIVER_ADDR = ('::1', 10001)
SENDER_ADDR = ('::1', 10002)
PROXY_ADDR = ('::1', 10003)


def receiver():
    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sock.bind(RECEIVER_ADDR)

        with open("./files/new_file_1.pdf", 'wb') as file:
            buffer = sock.recv(1024)
            while buffer:
                if (buffer.find(bytes('EOF-EOF-EOF-EOF-EOF', 'utf-8')) != -1):
                    break

                file.write(buffer)
                buffer = sock.recv(1024)

    except Exception as ex:
        print(ex)
    finally:
        sock.close()


if __name__ == '__main__':
    receiver()