import socket
import time
import statistics

RECEIVER_ADDR = ('127.0.0.1', 10001)
SENDER_ADDR = ('127.0.0.2', 10002)
PROXY_ADDR = ('127.0.0.3', 10003)
SECOND_RECEIVER_ADDR = ('127.0.0.4', 10004)

MESSAGE = "@COVER sdfsfdsf!@"

DEFAULT_DELAY = 0.01


def to_bits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


def proxy():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(PROXY_ADDR)

        not_sent = True

        packets_time_list = []
        message = to_bits(MESSAGE)
        it = iter(range(len(message)))

        counter = -1
        median = -1

        while True:
            buffer = sock.recv(1024)

            if buffer.find(bytes('EOF-EOF-EOF-EOF-EOF', 'ascii')) != -1:
                sock.sendto(buffer, RECEIVER_ADDR)
                break

            counter += 1

            if counter < 200:
                time.sleep(DEFAULT_DELAY)
                packets_time_list.append(time.time())
                sock.sendto(buffer, RECEIVER_ADDR)

            elif not_sent:
                if median == -1:
                    intervals = [j - i for i, j in zip(packets_time_list[:-1], packets_time_list[1:])]
                    median = statistics.median(intervals)
                    print(median)

                try:
                    bit = message[next(it)]
                except StopIteration:
                    not_sent = False
                    time.sleep(DEFAULT_DELAY)
                    sock.sendto(buffer, RECEIVER_ADDR)
                    continue

                if bit == 0:
                    time.sleep(median + DEFAULT_DELAY)

                sock.sendto(buffer, RECEIVER_ADDR)

            else:
                time.sleep(DEFAULT_DELAY)
                sock.sendto(buffer, RECEIVER_ADDR)

    except Exception as ex:
        print(ex)

    finally:
        sock.close()


if __name__ == '__main__':
    proxy()
