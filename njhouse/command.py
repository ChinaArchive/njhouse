# coding:utf-8

from json import dumps
from logging import DEBUG
import os
from typing import Dict
from typing import Optional
from typing import Sequence

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from .attribute import __project__
from .attribute import __urlhome__
from .attribute import __version__
from .service import run as njhouse_run
from .utils import njhouse_query
from .utils import njhouse_store


@add_command("service", help="Web Service")
def add_cmd_service(_arg: argp):
    _arg.add_argument("-a", "--address", dest="ip_address", type=str,
                      metavar="ADDR", default="0.0.0.0",
                      help="The default IP address is 0.0.0.0")
    _arg.add_argument("-p", "--port", dest="port", type=int,
                      metavar="PORT", default=8025,
                      help="The default port is 8025")


@run_command(add_cmd_service)
def run_cmd_service(cmds: commands) -> int:
    addr: str = cmds.args.ip_address
    port: int = cmds.args.port
    debug: bool = cmds.logger.level <= DEBUG
    njhouse_run(host=addr, port=port, debug=debug)
    return 0


@add_command("query", help="查询数据")
def add_cmd_query(_arg: argp):
    pass


@run_command(add_cmd_query)
def run_cmd_query(cmds: commands) -> int:
    result: Dict[str, Dict[str, int]] = njhouse_query().dict_all()
    cmds.stdout(dumps(result, ensure_ascii=False, indent=2))
    return 0


@add_command("store", help="存储数据")
def add_cmd_store(_arg: argp):
    _arg.add_argument("-d", "--dir", dest="directory", type=str,
                      metavar="DIR", default=".", help="存储目录")


@run_command(add_cmd_store)
def run_cmd_store(cmds: commands) -> int:
    directory: str = os.path.abspath(cmds.args.directory)
    njhouse_store(directory=directory).save()
    return 0


@add_command(__project__)
def add_cmd(_arg: argp):
    pass


@run_command(add_cmd, add_cmd_service, add_cmd_query, add_cmd_store)
def run_cmd(cmds: commands) -> int:
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(
        root=add_cmd,
        argv=argv,
        description="抓取 njhouse.com.cn 数据",
        epilog=f"For more, please visit {__urlhome__}.")
