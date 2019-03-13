#!/usr/bin/env python3

import json
import signal
import sys


def handler(signum, frame):
    print('Operation Timed Out', file=sys.stderr)
    exit(99)


def process_check():
    signal.alarm(5)

    try:
        with sys.stdin as standard_in:
            request = json.load(standard_in)

        if request is None:
            print('No configuration provided', file=sys.stderr)
            exit(1)
        else:
            version_list = [request['version']]
            print(version_list)

    except SystemExit:
        print('System Exit detected', file=sys.stderr)


def main():
    signal.signal(signal.SIGALRM, handler)

    process_check()


if __name__ == '__main__':
    exit(main())
