#! /usr/bin/env python3
import re

from argparse import ArgumentParser
from subprocess import Popen, PIPE

from clipboard import copy
from pyotp import TOTP


PASS_COMMAND = "pass"


def main():
    parser = ArgumentParser(
        description="Command line tool to generate one-time passwords")
    parser.add_argument("ident")
    parser.add_argument("--copy", "-c",  action="store_true", default=False)
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
    proc = Popen([PASS_COMMAND, ident], stdout=PIPE)
    lines = proc.stdout.readlines()
    return lines


def get_secret_from_lines(lines):
    otp_secret = None

    for line in lines:
        line = line.decode()
        if re.match("^OTP:*", line, re.I):
            remain = line[4:].strip()
            otp_secret = remain.replace(" ", "")
            break

    return otp_secret


if __name__ == '__main__':
    main()
