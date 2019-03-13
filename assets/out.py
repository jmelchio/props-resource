#!/usr/bin/env python3

import json
import os
import signal
import sys


def handler(signum, frame):
    print('Operation Timed Out', file=sys.stderr)
    exit(1)


def process_out(directory=None):
    signal.alarm(5)

    try:
        with sys.stdin as standard_in:
            request = json.load(standard_in)

        if request is None:
            print('No configuration provided', file=sys.stderr)
            exit(1)
        else:
            props_path = request['params']['props_path']
            with open(os.path.join(directory, props_path), 'r') as props_file:
                gradle_props = json.load(props_file)

            out = {
                'version': gradle_props['version'],
                'metadata': [
                    {'name': 'gradle_props', 'value': gradle_props}
                ]
            }

            print(out)

    except SystemExit:
        print('System Exit detected', file=sys.stderr)
        exit(124)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        print('Usage: %s PATH' % argv[0], file=sys.stderr)
        exit(1)

    signal.signal(signal.SIGALRM, handler)

    process_out(argv[1])


if __name__ == '__main__':
    exit(main())
