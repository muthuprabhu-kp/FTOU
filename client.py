import os
import socket
import time
import sys

HOST_IP = "127.0.0.1"
TCP_PORT = 23232
buf = 1024 - 100
file_name = sys.argv[1]


def get_header(data):
    header_string = data[:100].decode('utf-8')
    return dict(item.split(':') for item in header_string.split(';') if item and ':' in item)


def send(host, port):
    part = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.sendto(file_name, (UDP_IP, UDP_PORT))
    print("Sending %s ..." % file_name)
    file_size = os.path.getsize(file_name)
    file = file_name.split("/")[-1]
    f = open(file_name, "rb")
    remaining_part = file_size / buf
    header = (bytes(f"PRT:{str(part)};RPRT:{remaining_part};FLE:{file};SZE:{file_size};", 'utf-8') + b"\0" * 100)[:100]
    data = f.read(buf)
    while data:
        if sock.sendto(header + data, (host, int(port))):
            data = f.read(buf)
            part += 1
            header = (bytes(f"HDR:{str(part)};RPRT:{remaining_part - part};FLE:{file};SZE:{file_size};",
                            'utf-8') + b"\0" * 100)[:100]
            # time.sleep(0.02)  # Give receiver a bit time to save

    sock.close()
    f.close()


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
        tcp_sock.connect((HOST_IP, TCP_PORT))
        while True:
            data = tcp_sock.recv(1024)
            if not data:
                break
            header = get_header(data)
            print(header)
            if header['TYP'] == 'ACK':
                print(f'Received ACK for {header["PRT"]}')
            if header['TYP'] == 'UDP':
                send(header['HST'], header['PRT'])


if __name__ == '__main__':
    client()
