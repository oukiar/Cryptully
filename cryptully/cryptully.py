#! /usr/bin/env python2.7

import sys
import signal
import argparse

from utils import constants

from ncurses.ncurses import NcursesUI
from qt.qt import QtUI


ncursesUI = None
qtUI = None


def main():
    args = parse_cmdline_args()

    signal.signal(signal.SIGINT, signalHandler)

    if args.ncurses:
        global ncursesUI
        ncursesUI = NcursesUI(args.mode, args.port, args.host)
        ncursesUI.start()
    else:
        global qtUI
        qtUI = QtUI(sys.argv, args.mode, args.port, args.host)
        qtUI.start()

    sys.exit(0)


def parse_cmdline_args():
    argvParser = argparse.ArgumentParser()
    argvParser.add_argument('-p', '--port', dest='port', nargs='?', type=int, default=str(constants.DEFAULT_PORT), help="Port to connect listen on (server) or connect to (client).")
    argvParser.add_argument('-s', '--server', dest='server', default=False, action='store_true', help="Run as server.")
    argvParser.add_argument('-c', '--client', dest='client', default=False, action='store_true', help="Run as client.")
    argvParser.add_argument('-n', '--ncurses', dest='ncurses', default=False, action='store_true', help="Use the NCurses UI.")
    argvParser.add_argument('host', nargs='?', help="The host to connect to (if client)")

    args = argvParser.parse_args()

    # Set the mode from the client and server command line args. If neither were specified, let the UI ask the user later
    if args.client:
        args.mode = constants.MODE_CLIENT
    elif args.server:
        args.mode = constants.MODE_SERVER
    else:
        args.mode = None

    # Check the port range
    if args.port <= 0 or args.port > 65536:
        print "The port must be between 1 and 65536 inclusive."
        sys.exit(1)

    # Ncurses is not supported on Windows
    if sys.platform is 'win32' and args.ncurses:
        print "Ncurses is not supported on Windows."
        sys.exit(1)

    return args


def signalHandler(signal, frame):
    if ncursesUI is not None:
        ncursesUI.stop()
    if qtUI is not None:
        qtUI.stop()
    sys.exit(0)


if __name__ == "__main__":
    main()
