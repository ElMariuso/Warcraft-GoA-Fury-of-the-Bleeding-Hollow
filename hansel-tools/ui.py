"""Helpers d'affichage terminal (ANSI) partagés entre tous les scripts."""

import sys

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"


def colored(msg: str, color: str) -> str:
    return f"{color}{msg}{RESET}"


def info(msg: str) -> None:
    print(f"{CYAN}{msg}{RESET}")


def success(msg: str) -> None:
    print(f"{GREEN}{msg}{RESET}")


def warn(msg: str) -> None:
    print(f"{YELLOW}{msg}{RESET}")


def error(msg: str) -> None:
    print(f"{RED}{msg}{RESET}", file=sys.stderr)


def dim(msg: str) -> None:
    print(f"{DIM}{msg}{RESET}")
