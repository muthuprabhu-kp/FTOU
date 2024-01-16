import uuid
from queue import Queue

from pysondb import db

from Server.util.Auth import Auth
from Server.util.Config import Config


class Session:
    def __init__(self):
        self.config = None
        self.db = None
        self.auth = None
        self.session_id = {}
        self.queue = {}

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

    def is_valid_user(self, auth_data):
        if 'SID' in auth_data:
            sid = auth_data.get('SID')
            if sid in self.session_id:
                return sid, self.session_id.get(sid)
        is_valid, user = self.get_auth().is_valid_user(auth_data)
        if is_valid:
            sid = self.generate_session_id(user)
            return sid, user
        return False

    def invalidate_session_id(self, uid):
        prev_session = [k for k, v in self.session_id.items() if v.get_user_id() != uid]
        if prev_session:
            self.queue = {k: v for k, v in self.queue.items() if k != prev_session[0]}
        self.session_id = {k: v for k, v in self.session_id.items() if v.get_user_id() != uid}

    def get_queue_by_id(self, sid):
        return self.queue.get(sid)

    def generate_session_id(self, user):
        uid = user.get_user_id()
        self.invalidate_session_id(uid)
        sid = str(uuid.uuid4().fields[-1])[:5]
        self.session_id[sid] = user
        self.queue[sid] = Queue()
        return sid

    def get_auth(self):
        if not self.auth:
            jdb = self.get_db()
            self.auth = Auth(jdb)
        return self.auth
