import getopt
import sys

from Server.FTOUServer import Server
from Server.RequestHandler import RequestHandler
from Server.util.Session import Session


def get_args():
    options = "hc:"
    argument_list = sys.argv[1:]
    long_options = ["Help", "Config="]
    config_path = './server-config.toml'
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argument_list, options, long_options)

        # checking each argument
        for current_argument, current_value in arguments:

            if current_argument in ("-h", "--Help"):
                print("Displaying Help")
            elif current_argument in ("-c", "--Config"):
                print("Loading Config from path (% s)".format(current_value))
                config_path = current_value
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
    return config_path


def start():
    try:
        config_path = get_args()
        session = Session()
        session.init(config_path)
        with Server(RequestHandler, session) as server:
            server.serve_forever()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    start()
