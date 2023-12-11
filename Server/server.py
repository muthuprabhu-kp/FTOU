import os
import random
import socket
import toml
import time
import sys

from ByteSequencer import Sequencer

SERVER_IP = "127.0.0.1"
UDP_PORT_RANGE = list(range(5000, 6000))
TCP_PORT = 23232

sequence_manager = {}


def get_sequence_obj(name):
    if name not in sequence_manager:
        sequence_manager[name] = Sequencer(name)
    return sequence_manager.get(name)


def get_header(data):
    header_string = data[:100].decode('utf-8')
    return dict(item.split(':') for item in header_string.split(';') if item and ':' in item)


def get_byte_object(data):
    byte_obj = data[100:]
    header = get_header(data)
    return {
        'index': int(header['PRT']),
        'last': int(header['PRT']),
        'data': byte_obj
    }


def send_ack(tcp_conn, prt):
    tcp_conn.send((bytes(f'PRT:{prt};TYP:ACK;', 'utf-8') + b"\0" * 100)[:100])


def server():
    print(f'Listening on: {SERVER_IP}:{TCP_PORT}')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
        tcp_sock.bind((SERVER_IP, TCP_PORT))
        tcp_sock.listen()
        conn, addr = tcp_sock.accept()
        with conn:
            print(f"Connected by {addr}")
            udp_port = random.choice(UDP_PORT_RANGE)
            udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_sock.bind((SERVER_IP, udp_port))
            conn.send((bytes(f'TYP:UDP;PRT:{udp_port};HST:{SERVER_IP};', 'utf-8') + b"\0" * 100)[:100])
            while True:
                data, uaddr = udp_sock.recvfrom(1024)
                if uaddr[0] != addr[0] or not data:
                    break
                header = get_header(data)
                send_ack(conn, header.get('PRT'))
                bye_obj = get_byte_object(data)
                seq = get_sequence_obj(addr[0] + ':' + header['FLE'])
                seq.add(bye_obj)
                # data = conn.recv(1024)


                #conn.sendall(data)

if __name__ == '__main__':
    server()
