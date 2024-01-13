import logging
import socketserver


class RequestHandler(socketserver.BaseRequestHandler):
    def setup(self) -> None:
        logging.info("Start request.")

    def get_auth_data(self, data):
        auth_string = data.decode('utf-8')
        auth_data = dict(item.split(':') for item in auth_string.split(';') if item and ':' in item)
        return auth_data

    def handle(self) -> None:
        conn = self.request
        session = self.server.session
        auth = session.get_auth()
        while True:
            data = conn.recv(1024)
            auth_param = self.get_auth_data(data)
            is_valid, user = auth.is_valid_user(auth_param)
            if not is_valid:
                logging.info("Invalid User")
                conn.send((bytes(f'TYP:AUTH;STS:401;MSG:LoginFailed;', 'utf-8') + b"\0" * 100)[:100])
                break
            logging.info("Valid User")
            conn.send((bytes(f'TYP:AUTH;STS:200;MSG:LoggedInSuccessfully;', 'utf-8') + b"\0" * 100)[:100])

            #logging.info(f"recv: {data!r}")
            #conn.sendall(data)

    def finish(self) -> None:
        logging.info("Finish request.")
