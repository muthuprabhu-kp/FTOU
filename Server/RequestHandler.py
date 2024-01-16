import logging
import socketserver

from Server.Shell.UserShell import Shell


class RequestHandler(socketserver.BaseRequestHandler):
    def setup(self) -> None:
        logging.info("Start request.")

    def get_auth_data(self, data):
        auth_string = data.decode('utf-8')
        auth_data = dict(item.split(':') for item in auth_string.split(';') if item and ':' in item)
        return auth_data

    def handle(self) -> None:
        while True:
            conn = self.request
            session = self.server.session
            # auth = session.get_auth()
            data = conn.recv(1024)
            data_param = self.get_auth_data(data)
            r_type = data_param['TYP']
            sid, user = session.is_valid_user(data_param)
            if r_type.strip() == "AUTH":
                if not sid:
                    logging.info("Invalid User")
                    conn.send((bytes(f'TYP:AUTH;STS:401;MSG:LoginFailed;', 'utf-8') + b"\0" * 100)[:100])
                    continue
                logging.info("Valid User")
                conn.send((bytes(f'TYP:AUTH;STS:200;MSG:LoggedInSuccessfully;SID:{sid}', 'utf-8') + b"\0" * 100)[:100])
                continue
            if not sid:
                continue
            s = Shell(user, conn, data_param)
            s.start()
            s.join()
        """if r_type == "CMD":
            q = session.get_queue_by_id(sid)
            if q:
                q.put(data_param)"""

    def finish(self) -> None:
        logging.info("Finish request.")
