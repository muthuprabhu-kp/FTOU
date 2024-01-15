class User:
    def __init__(self, info):
        self.info = info

    def get_user_home(self):
        return self.info.get("home") or f"{self.info['user_id']}/"

    def get_user_id(self):
        return self.info['user_id']
