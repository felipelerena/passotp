#! /usr/bin/env python3
import re

from argparse import ArgumentParser
from datetime import datetime
from subprocess import Popen, PIPE
from sys import stdin

from clipboard import copy
from pyotp import TOTP


PASS_COMMAND = "pass"


def main():
    """ Main function for the script."""
    # Find out if the command was called via pipe
    isatty = stdin.isatty()
    parser = ArgumentParser(
        description="Command line tool to generate one-time passwords")
    # If it's not a pipe the ident argument is not required there's not a more
    # elegant way to do this AFAIK
    if isatty:
        parser.add_argument("ident", help="The stored password name.")
    parser.add_argument("--copy", "-c",  action="store_true", default=False,
                        help="Copy to clipboard.")
    args = parser.parse_args()

    if isatty:
        # Getting the lines from the password storage
        lines = get_lines(args.ident)
    else:
        # Getting the lines from the stdin
        lines = stdin.readlines()

    secret = get_secret_from_lines(lines)
    if secret is not None:
        otp = TOTP(secret).now()

        if args.copy:
            copy(otp)
        else:
            print(otp)
        seconds = (60 - datetime.now().second) % 30
        print("Seconds remaing: {}".format(seconds))
    else:
        print("No OTP secret found.")


def get_lines(ident):
    """Returns the decrypted lines for the password files.

    Arguments:
        ident -- the stored password name.
    """
    proc = Popen([PASS_COMMAND, ident], stdout=PIPE)
    lines = proc.stdout.readlines()
    return lines


def get_secret_from_lines(lines):
    """Get the OTP secret from the config lines.

    Arguments:
        lines -- the config lines for the password file.
    """
    otp_secret = None

    for line in lines:
        try:
            line = line.decode()
        except AttributeError:
            # if the line come from the stdin the line is a string instead of a
            # bytestream
            pass
        if re.match("^OTP:*", line, re.I):
            remain = line[4:].strip()
            # the secret is usually show in letter groups separated with spaces
            # we shoud get rid of those spaces.
            otp_secret = remain.replace(" ", "")
            break

    return otp_secret


if __name__ == '__main__':
    main()
