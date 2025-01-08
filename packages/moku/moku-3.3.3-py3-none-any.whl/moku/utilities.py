import re
from subprocess import PIPE, Popen

from .exceptions import InvalidParameterRange, MokuException, MokuNotFound
from .finder import Finder


def find_moku_by_serial(serial):
    result = Finder().find_all(timeout=10, filter=lambda x: x.serial == serial)
    if len(result) > 0:
        return result[0].ipv4_addr
    raise MokuNotFound()


def check_mokucli_version(cli_path, req_ver=None):
    if cli_path:
        out, _ = Popen([cli_path, "--version"], stdout=PIPE, stderr=PIPE).communicate()
        if out:
            if not req_ver:
                return
            ver_str = out.decode("utf8").rstrip()
            installed_ver = tuple(
                [int(x) for x in re.split(r"\D+", ver_str) if x.isdigit()]
            )
            if installed_ver >= req_ver:
                return

    req_ver_str = f"{req_ver[0]}.{req_ver[1]}.{req_ver[2]}" if req_ver else ""
    raise MokuException(
        f"Cannot find mokucli {req_ver_str}. \n"
        "Please download latest version of the CLI from https://www.liquidinstruments.com/software/utilities/. \n"  # noqa
        "If you have already installed, please set the MOKU_CLI_PATH environment variable to absolute path of mokucli."
    )  # noqa
