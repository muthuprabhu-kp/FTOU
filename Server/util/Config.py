from pysondb import db
import toml


class Config:
    def __init__(self, path):
        self.config = None
        self.db = None
        self.load_config(path)

    def load_config(self, path):
        config = {}
        with open(path, 'r') as f:
            config = toml.load(f)
        self.config = config

    def get_db_path(self):
        return self.config['db']['path']

    def get_socket_host(self):
        return self.config['server']['host']

    def get_socket_port(self):
        return self.config['server']['port']

    def get_udp_range(self):
        udp_range = self.config['server']['udp_port_range']
        udp_range_list = udp_range.split('-')
        return list(range(int(udp_range_list[0]), int(udp_range_list[1])))

    def is_ssl_enabled(self):
        is_ssl_enabled = self.config['ssl']['enabled']
        return is_ssl_enabled

    def get_cert_chain(self):
        return self.config['ssl'].get('cert_chain', None)

    def get_private_key(self):
        return self.config['ssl']['private_key']
