#!/usr/bin/env python3
"""
Linux Security Monitor
----------------------

Monitors:
- /var/log/auth.log
- /var/log/syslog

Detects:
- Failed SSH logins
- Successful SSH logins
- Invalid users
- Interactive root shell commands from syslog

Run:
    sudo python3 security_monitor.py
"""

import sys
import os
import re
import time
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

AUTH_LOG = sys.argv[1]
SYSLOG = sys.argv[2]

POLL_INTERVAL = 0.2

# ============================================================
# COLORS
# ============================================================

RESET = "\033[0m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
BOLD = "\033[1m"

# Enable ANSI colors on Windows
if os.name == "nt":
    os.system("")

# ============================================================
# REGEX
# ============================================================

IP_REGEX = r"(?:\d{1,3}\.){3}\d{1,3}"

FAILED_LOGIN = re.compile(
    rf"Failed password for(?: invalid user)? (\S+) from ({IP_REGEX})"
)

ACCEPTED_LOGIN = re.compile(
    rf"Accepted \S+ for (\S+) from ({IP_REGEX})"
)

INVALID_USER = re.compile(
    rf"Invalid user (\S+) from ({IP_REGEX})"
)

# Example:
# 2026-05-07 ... [root] 172.17.0.1 ... : cat /etc/passwd
ROOT_COMMAND = re.compile(
    rf"\[(.*?)\]\s+({IP_REGEX}).*?:\s+(.*)"
)

# ============================================================
# FILE TAILER
# ============================================================

class FileTail:
    def __init__(self, path):
        self.path = Path(path)
        self.file = None
        self.position = 0
        self.inode = None

    def open(self):
        while True:
            try:
                self.file = open(
                    self.path,
                    "r",
                    encoding="utf-8",
                    errors="replace"
                )

                # Start at end
                self.file.seek(0, os.SEEK_END)
                self.position = self.file.tell()

                stat = os.stat(self.path)
                self.inode = getattr(stat, "st_ino", None)

                print(
                    f"{YELLOW}[WATCHING]{RESET} {self.path}"
                )

                return

            except FileNotFoundError:
                print(
                    f"{RED}[WAITING]{RESET} {self.path} not found"
                )
                time.sleep(1)

    def check_rotation(self):
        try:
            stat = os.stat(self.path)

            inode = getattr(stat, "st_ino", None)

            # File rotated
            if inode != self.inode:
                self.file.close()
                self.open()
                return

            # File truncated
            if stat.st_size < self.position:
                self.file.seek(0)
                self.position = 0

        except FileNotFoundError:
            pass

    def read_new_lines(self):
        self.check_rotation()

        self.file.seek(self.position)

        lines = self.file.readlines()

        if lines:
            self.position = self.file.tell()

        return lines


# ============================================================
# OUTPUT
# ============================================================

def print_failed_login(user, ip):
    print(
        f"{RED}{BOLD}[FAILED LOGIN]{RESET} "
        f"user={YELLOW}{user}{RESET} "
        f"ip={CYAN}{ip}{RESET}",
        flush=True
    )


def print_success_login(user, ip):
    print(
        f"{GREEN}{BOLD}[LOGIN SUCCESS]{RESET} "
        f"user={YELLOW}{user}{RESET} "
        f"ip={CYAN}{ip}{RESET}",
        flush=True
    )


def print_invalid_user(user, ip):
    print(
        f"{MAGENTA}{BOLD}[INVALID USER]{RESET} "
        f"user={YELLOW}{user}{RESET} "
        f"ip={CYAN}{ip}{RESET}",
        flush=True
    )


def print_root_command(user, ip, command):
    print(
        f"{WHITE}{BOLD}[ROOT COMMAND]{RESET} "
        f"user={YELLOW}{user}{RESET} "
        f"ip={CYAN}{ip}{RESET} "
        f"cmd={GREEN}{command}{RESET}",
        flush=True
    )


# ============================================================
# PARSERS
# ============================================================

def parse_auth_line(line):

    # Failed login
    match = FAILED_LOGIN.search(line)
    if match:
        user, ip = match.groups()
        print_failed_login(user, ip)
        return

    # Successful login
    match = ACCEPTED_LOGIN.search(line)
    if match:
        user, ip = match.groups()
        print_success_login(user, ip)
        return

    # Invalid user
    match = INVALID_USER.search(line)
    if match:
        user, ip = match.groups()
        print_invalid_user(user, ip)
        return


def parse_syslog_line(line):

    match = ROOT_COMMAND.search(line)

    if not match:
        return

    user, ip, command = match.groups()

    # Ignore empty/noisy commands
    ignored = [
        "PROMPT_COMMAND",
        "history -a",
    ]

    for item in ignored:
        if item in command:
            return

    print_root_command(user, ip, command.strip())


# ============================================================
# MAIN
# ============================================================

def main():

    auth = FileTail(AUTH_LOG)
    syslog = FileTail(SYSLOG)

    auth.open()
    syslog.open()

    print(
        f"\n{BOLD}Linux Security Monitor Started{RESET}\n"
    )

    while True:

        # auth.log
        for line in auth.read_new_lines():
            parse_auth_line(line)

        # syslog
        for line in syslog.read_new_lines():
            parse_syslog_line(line)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(f"\n{YELLOW}Stopped.{RESET}")