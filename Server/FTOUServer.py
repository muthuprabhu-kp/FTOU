import logging
import socket
import socketserver
import ssl
import time

logging.basicConfig(level=logging.INFO)


class Server(socketserver.ThreadingTCPServer):
    _timeout = 5  # seconds
    _start_time = time.monotonic()

    def __init__(self, request_handler_class, session):
        super().__init__(session.get_socket_address(), request_handler_class)
        self.session = session
        self.private_key = None
        self.cert_chain = None
        self.is_ssl_enabled = None
        self.load_session()

    def load_session(self):
        self.is_ssl_enabled = self.session.get_config().is_ssl_enabled()
        self.cert_chain = self.session.get_config().get_cert_chain()
        self.private_key = self.session.get_config().get_private_key()

    def server_activate(self) -> None:
        logging.info("Server started on %s:%s", *self.server_address)
        super().server_activate()

    def get_request(self) -> tuple[socket.socket, str]:
        conn, addr = super().get_request()
        logging.info("Connection from %s:%s", *addr)
        if self.is_ssl_enabled:
            logging.info("Wrapping in TLS")
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(self.cert_chain, self.private_key)
            return context.wrap_socket(conn, server_side=True), addr
        return conn, addr

    def service_actions(self) -> None:
        if time.monotonic() - self._start_time > self._timeout:
            logging.info("Server paused, something else is running...")
            self._start_time = time.monotonic()
