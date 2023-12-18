from pysondb import db
import rsa


class Auth:
    def __init__(self, path):
        self.db = db.getDb(path)
        pass

    def is_valid_user(self, signature, auth_data):
        user_info = self.db.getBy({"user_id": auth_data['user_id']})
        if not user_info:
            return False
        key = user_info['key']
        try:
            rsa.verify(auth_data, signature, key)
        except Exception as e:
            print(e)
            return False
        return True
