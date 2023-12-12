import getopt
import random
import socket
import sys

import toml

from Server.ByteSequencer import Sequencer

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


def start_server(config):
    server_ip = config['SERVER']['SERVER_IP']
    tcp_port = config['SERVER']['TCP_PORT']
    udp_port_range = config['SERVER']['UDP_PORT_RANGE']
    print(f'Listening on: {server_ip}:{tcp_port}')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
        tcp_sock.bind((server_ip, tcp_port))
        tcp_sock.listen()
        conn, addr = tcp_sock.accept()
        with conn:
            print(f"Connected by {addr}")
            udp_port = random.choice(udp_port_range)
            udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_sock.bind((server_ip, udp_port))
            conn.send((bytes(f'TYP:UDP;PRT:{udp_port};HST:{server_ip};', 'utf-8') + b"\0" * 100)[:100])
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

                # conn.sendall(data)


if __name__ == '__main__':
    config = {}
    options = "hc:"
    argumentList = sys.argv[1:]
    long_options = ["Help", "Config="]
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)

        # checking each argument
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--Help"):
                print("Displaying Help")
            elif currentArgument in ("-c", "--Config"):
                print("Enabling special output mode (% s)".format(currentValue))
                with open(currentValue, 'r') as f:
                    config = toml.load(f)

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
    start_server(config)
