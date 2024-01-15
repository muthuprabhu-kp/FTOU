from threading import Thread

from Server.Shell.DirectoryService import DirectoryService


class Shell(Thread):
    def __init__(self, user, conn, data):
        Thread.__init__(self)
        self.user = user
        self.command = Command(user)
        self.conn = conn
        self.data = data

    def run(self):
        try:
            # command_str = conn.recv(1024)
            command = self.command.parse_command(self.data)
            if not command:
                self.conn.send((bytes('Invalid Command', 'utf-8') + b"\0" * 100)[:100])
            response = self.command.get_command(command)
            self.conn.sendall(response.encode())

        except Exception as e:
            self.conn.sendall(str(e).encode())


class Command:
    def __init__(self, user):
        self.directory_service = DirectoryService(user)

    def parse_command(self, data):
        # header_string = data[:100].decode('utf-8')
        # data = dict(item.split(':') for item in header_string.split(';') if item and ':' in item)
        if data['TYP'] != 'CMD':
            return []
        raw_command = data['CMD']
        command_split = raw_command.split(' ')
        return

    def get_command(self, command):
        action = None
        match command:
            case "ls":
                action = self.directory_service.ls()
            case _:
                action = None
        return action
