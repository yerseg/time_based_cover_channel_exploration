import socket
import statistics
import time

RECEIVER_ADDR = ('127.0.0.1', 10001)
SENDER_ADDR = ('127.0.0.2', 10002)
PROXY_ADDR = ('127.0.0.3', 10003)
SECOND_RECEIVER_ADDR = ('127.0.0.4', 10004)

EPSILON = 0.005


def from_bits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def receiver():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(RECEIVER_ADDR)

        packets_time_list = []
        message = []

        idx = 0

        median = -1
        counter = -1

        prev_time = 0
        curr_time = 0

        while True:
            buffer = sock.recv(1024)
            if buffer.find(bytes('EOF-EOF-EOF-EOF-EOF', 'ascii')) != -1:
                break

            counter += 1

            if counter < 180:
                packets_time_list.append(time.time())
                continue

            if median == -1:
                intervals = [j - i for i, j in zip(packets_time_list[:-1], packets_time_list[1:])]
                median = statistics.median(intervals)
                curr_time = time.time()
                continue

            prev_time = curr_time
            curr_time = time.time()

            interval = curr_time - prev_time

            if abs(interval - median) >= EPSILON:
                message.append(1 if interval - median < 0 else 0)

            print("interval - ", interval, ", ", curr_time, ", ", prev_time)
            print(buffer)

        print(from_bits(message))

    except Exception as ex:
        print(ex)
    finally:
        sock.close()


if __name__ == '__main__':
    receiver()