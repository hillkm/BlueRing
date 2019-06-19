import configparser
import logging
from pytoxcore import ToxCore
import time

logging.basicConfig(level=logging.DEBUG)

class BlueRing(ToxCore):
    def __init__(self):
        self.options = {}
        loader = configparser.ConfigParser()
        loader.read('BlueRing.ini')
        file_opts = loader['BlueRing']

        self.options["ipv6_enabled"] = file_opts.getboolean("ipv6_enabled")
        self.options["udp_enabled"] = file_opts.getboolean("udp_enabled")
        self.options["bootstrap_node"] = file_opts["bootstrap_node"]
        self.options["bootstrap_port"] = int(file_opts["bootstrap_port"])
        self.options["bootstrap_key"]  = file_opts["bootstrap_key"]

        super(BlueRing, self).__init__(self.options)
        self.tox_self_set_name("BlueRing Client")
        self.tox_self_set_status_message("Alpha Testing")

    def bootstrap(self):
        logging.debug(f'Attempting bootstrap: Node @ {self.options["bootstrap_node"]}'
                      f':{self.options["bootstrap_port"]}, key: {self.options["bootstrap_key"]}')
        self.tox_bootstrap(self.options["bootstrap_node"], self.options["bootstrap_port"],
                           self.options["bootstrap_key"])
        logging.debug(f'After bootstrap attempt, connection status is: {self.tox_self_get_connection_status()}')

    def run(self):
        self.bootstrap()

        print(f"Connected, using ToxID {self.tox_self_get_address()}")
        disconnectionCheck = False
        iteration_interval = self.tox_iteration_interval()

        while True:
            if not disconnectionCheck and self.tox_self_get_connection_status() != ToxCore.TOX_CONNECTION_NONE:
                disconnectionCheck = True

            if disconnectionCheck and self.tox_self_get_connection_status() == ToxCore.TOX_CONNECTION_NONE:
                logging.debug(f"Connection interrupted: attempting bootstrap reconnect")
                self.bootstrap()
                disconnectionCheck = False

            self.tox_iterate()
            time.sleep(float(iteration_interval) / 100.0)


    def tox_friend_message_cb(self, friend_number, message):
        friend_name = self.tox_friend_get_name(friend_number)
        print(f"{friend_name}: {message}")
        string = input("... ")

        outbox = self.tox_friend_send_message(friend_number, ToxCore.TOX_MESSAGE_TYPE_NORMAL, string)
        print(f"{self.tox_self_get_name()}: {outbox}")
        logging.debug(f"{self.tox_self_get_name()}: {outbox}")

    def tox_friend_request_cb(self, public_key, message):
        logging.debug(f"Friend request\n{public_key}: {message}")
        self.tox_friend_add_norequest(public_key)
        logging.debug(f"Friend added")

    # The following functions
    #         tox_friend_status_cb()
    #         send_avatar()
    #         send_file()
    #         tox_friend_read_receipt_cb()
    #         can_accept_file()
    # Are not strictly necessary for the program to run -- but without them, the tox_iterate loop will sometimes hang

    def tox_friend_status_message_cb(self, friend_number, message):
        print(f"{self.tox_friend_get_name(friend_number)} is now {message}")

    def tox_friend_status_cb(self, friend_number, status):
        # print(f"{self.tox_friend_get_name(friend_number)} is now {status}")
        pass

    def send_avatar(self, friend_number):
        pass

    def send_file(self, friend_number, path, name=None):
        pass

    def tox_friend_read_receipt_cb(self, friend_number, message_id):
        pass

    def can_accept_file(self, friend_number, file_number, kind, file_size, filename):
        pass

    def tox_file_recv_cb(self, friend_number, file_number, kind, file_size, filename):
        pass


bluering = BlueRing()
bluering.run()