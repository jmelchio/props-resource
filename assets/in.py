#!/usr/bin/env python3

import json
import os
import signal
import sys


def handler(signum, frame):
    print('Operation Timed Out', file=sys.stderr)
    exit(1)


def process_in(directory=None):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            print('Failed to create output directory: %s' % directory, file=sys.stderr)
            exit(1)

    signal.alarm(5)

    try:
        with sys.stdin as standard_in:
            request = json.load(standard_in)

        if request is None:
            print('No configuration provided', file=sys.stderr)
            exit(1)
        else:
            with open(os.path.join(directory, 'input.json'), 'w') as input_file:
                input_file.write(json.dumps(request))

        version = {'version': request['version']}
        print(version)

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

    process_in(argv[1])


if __name__ == '__main__':
    exit(main())
