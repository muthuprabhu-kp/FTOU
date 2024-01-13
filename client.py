import json
import os
import socket
import time
import sys
import ssl
from base64 import b64encode

import rsa

HOST_IP = "localhost"
USER_ID = "test123"
AUTH_KEY = "/home/hackers/easy-rsa/generated/generate_rsa_key/private1.pem"
TCP_PORT = 23232
buf = 1024 - 100
file_name = sys.argv[1]


def load_file(path) -> bytes:
    data = ''
    with open(path, 'rb') as f:
        data = f.read()
    return data


def get_auth_info():
    epoch_time = int(time.time())
    private_str = load_file(AUTH_KEY)
    private = rsa.PrivateKey.load_pkcs1(private_str)
    # private = rsa.pem.load_pem(private_str, b"RSA PRIVATE KEY")
    message = f"USER_ID:{USER_ID};TIM:{epoch_time};"
    # data = bytes(message, 'utf-8')
    signature = b64encode(rsa.sign(message.encode(), private, "SHA-256")).decode()
    return bytes(f"TYP: AUTH;USER_ID:{USER_ID};TIM:{epoch_time};SIG:{signature};", 'utf-8')


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
    context = ssl.create_default_context()
    # context.verify_mode = ssl.CERT_NONE
    context.load_verify_locations('/home/hackers/easy-rsa/generated/cert.crt')
    auth_info = get_auth_info()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
        tcp_sock.connect((HOST_IP, TCP_PORT))
        with context.wrap_socket(tcp_sock, server_hostname=HOST_IP) as ssock:
            print(ssock.version())
            while True:
                # send(header['HST'], header['PRT'])
                ssock.send((auth_info + b"\0" * 100)[:200])
                data = ssock.recv(1024)
                if not data:
                    break
                header = get_header(data)
                print(header)
                if header['TYP'] == 'AUTH' and header['STS'] == '200':
                    print(header['MSG'])
                if header['TYP'] == 'AUTH' and header['STS'] == '401':
                    print(header['MSG'])
                if header['TYP'] == 'ACK':
                    print(f'Received ACK for {header["PRT"]}')
                if header['TYP'] == 'UDP':
                    send(header['HST'], header['PRT'])


if __name__ == '__main__':
    # (pubkey, privkey) = rsa.newkeys(512)
    # a = open("/home/hackers/easy-rsa/generated/generate_rsa_key/private1.pem", "wb")
    # a.write(privkey.save_pkcs1())
    # a.close()
    # a = open("/home/hackers/easy-rsa/generated/generate_rsa_key/public1.pem", "wb")
    # a.write(pubkey.save_pkcs1())
    # a.close()
    client()
