#!/usr/bin/env python
import time
import arginit


class Echo(object):
    "Simple echo tool"

    def __init__(self, msg, repeat=10, interval=0.5):
        """
        Arguments:
            msg -- message body
            repeat -- time to echo
            interval -- interval seconds
        """
        self.message = msg
        self.repeat = int(repeat)
        self.interval = float(interval)

    def start(self):
        for i in range(self.repeat):
            print(self.message)
            time.sleep(self.interval)
        print("Done")


if __name__ == '__main__':
    service = arginit.create(Echo)
    service.start()
