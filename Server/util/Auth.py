import base64

from pysondb import db
import rsa

from Server.User import User


class Auth:
    def __init__(self, db):
        self.db = db
        pass

    def is_valid_user(self, auth_data):
        user_info = self.db.getBy({"user_id": auth_data['USER_ID']})
        signature = base64.b64decode(auth_data['SIG'])
        if not user_info:
            return False, None
        auth_info = f"USER_ID:{auth_data['USER_ID']};TIM:{auth_data['TIM']};"
        key = bytes(user_info[0]['key'], 'utf-8')
        try:
            public_key = rsa.PublicKey.load_pkcs1(key)
            rsa.verify(auth_info.encode(), signature, public_key)
        except Exception as e:
            print(e)
            return False, None
        return True, User(user_info[0])


if __name__ == '__main__':
    a = db.getDb('../../db')
    a.add({"user_id": "test123", "key": """-----BEGIN RSA PUBLIC KEY-----
MEgCQQCe5VYAGuD4V2wuE+XOnkjWQ40DBBxeCFF3wfxDVZgob4qkke30oBkrbRSV
TpFaVKxbVUahBfeDPUVTadOEL0yvAgMBAAE=
-----END RSA PUBLIC KEY-----"""})
