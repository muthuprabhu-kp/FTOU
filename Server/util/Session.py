from pysondb import db

from Server.util.Auth import Auth
from Server.util.Config import Config


class Session:
    def __init__(self):
        self.config = None
        self.db = None
        self.auth = None

    def init(self, path):
        self.config = Config(path)

    def get_db(self):
        if not self.db:
            path = self.config.get_db_path()
            self.db = db.getDb(path)
        return self.db

    def get_config(self):
        return self.config

    def get_socket_address(self):
        return self.config.get_socket_host(), self.config.get_socket_port()

    def get_auth(self):
        if not self.auth:
            jdb = self.get_db()
            self.auth = Auth(jdb)
        return self.auth
