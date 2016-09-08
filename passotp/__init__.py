#! /usr/bin/env python3
import re

from argparse import ArgumentParser
from subprocess import Popen, PIPE

from clipboard import copy
from pyotp import TOTP


PASS_COMMAND = "pass"


def main():
    """ Main function for the script."""
    parser = ArgumentParser(
        description="Command line tool to generate one-time passwords")
    parser.add_argument("ident", help="The stored password name.")
    parser.add_argument("--copy", "-c",  action="store_true", default=False,
                        help="Copy to clipboard.")
    args = parser.parse_args()

    lines = get_lines(args.ident)
    secret = get_secret_from_lines(lines)
    if secret is not None:
        otp = TOTP(secret).now()

        if args.copy:
            copy(otp)
        else:
            print(otp)
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
        line = line.decode()
        if re.match("^OTP:*", line, re.I):
            remain = line[4:].strip()
            # the secret is usually show in letter groups separated with spaces
            # we shoud get rid of those spaces.
            otp_secret = remain.replace(" ", "")
            break

    return otp_secret


if __name__ == '__main__':
    main()
