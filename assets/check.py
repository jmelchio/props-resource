#!/usr/bin/env python3

import json
import signal
import sys


def handler(signum, frame):
    print('Operation Timed Out', file=sys.stderr)
    exit(124)


def process_check():
    signal.alarm(5)

    try:
        try:
            with sys.stdin as standard_in:
                request = json.load(standard_in)
        except json.decoder.JSONDecodeError:
            print('No configuration provided', file=sys.stderr)
            exit(1)
        else:
            try:
                version = request['version']
                if len(version) == 0:
                    version = {"build_id": "0"}

                version_list = [version]
            except KeyError:
                version_list = [{"build_id": "0"}]

            print(json.dumps(version_list))

    except SystemExit:
        print('System Exit detected', file=sys.stderr)
        exit(124)


def main():
    signal.signal(signal.SIGALRM, handler)

    process_check()


if __name__ == '__main__':
    exit(main())
