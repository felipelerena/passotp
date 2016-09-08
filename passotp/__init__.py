#! /usr/bin/env python3

from argparse import ArgumentParser
from subprocess import Popen, PIPE

from clipboard import copy
from pyotp import TOTP


OTP_LINE_KEY = "OTP:"
PASS_COMMAND = "pass"


def main():
    parser = ArgumentParser(
        description="Command line tool to generate one-time passwords")
    parser.add_argument("ident")
    parser.add_argument("--copy", "-c",  action="store_true", default=False)
    args = parser.parse_args()

    lines = get_lines(args.ident)
    secret = get_secret_from_lines(lines)
    otp = TOTP(secret).now()

    if args.copy:
        copy(otp)
    else:
        print(otp)


def get_lines(ident):
    proc = Popen([PASS_COMMAND, ident], stdout=PIPE)
    lines = proc.stdout.readlines()
    return lines


def get_secret_from_lines(lines):
    otp_secret = None

    for line in lines:
        line = line.decode()
        if line.startswith(OTP_LINE_KEY):
            otp_secret = line[len(OTP_LINE_KEY):].strip()
            break

    return otp_secret


if __name__ == '__main__':
    main()
