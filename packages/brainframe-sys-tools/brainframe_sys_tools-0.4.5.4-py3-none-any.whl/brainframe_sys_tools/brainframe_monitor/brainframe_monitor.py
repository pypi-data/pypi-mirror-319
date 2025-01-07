#
# Copyright (c) 2021 Dilili Labs, Inc.  All rights reserved. Contains Dilili Labs Proprietary Information. RESTRICTED
# COMPUTER SOFTWARE.  LIMITED RIGHTS DATA.
#

import curses
from argparse import ArgumentParser

from brainframe_sys_tools.brainframe_monitor.benchmarker import Benchmarker
from brainframe_sys_tools.brainframe_monitor.fake_screen import FakeScreen
from brainframe_sys_tools.brainframe_monitor.report import Report
from datetime import datetime
from brainframe_sys_tools.command_utils import command, subcommand_parse_args, by_name


@command("fps_monitor")
def fps_monitor():
    version = "v2.0"
    args = _parse_args(version)
    no_screen = args.no_screen

    report = Report(
        times_hist_len=args.times_hist_len,
    )
    fps_hist_buf_len = args.duration / args.refresh_interval
    benchmarker = Benchmarker(
        version=version,
        fps_history_file=args.out,
        report=report,
        fps_hist_buf_len=fps_hist_buf_len,
        server_url=args.server_url,
        refresh_interval=args.refresh_interval,
    )
    time_0 = datetime.now()
    while True:
        try:
            if no_screen is None:
                curses.wrapper(benchmarker, time_0)
            else:
                screen = FakeScreen
                benchmarker.__call__(screen, time_0)
            break
        except curses.error:
            # This occurs when the terminal is too small
            pass


def _parse_args(version):
    parser = ArgumentParser(description=f"BrainFrame FPS Monitor {version}")
    parser.add_argument(
        "--refresh-interval",
        default=0.5,
        type=float,
        help=(
            "An interval to refresh results at. Values that are too low might effect "
            "result accuracy, default %(default)s"
        ),
    )
    parser.add_argument(
        "--times-hist-len",
        default=100,
        type=int,
        help="The number of zone status samples to wait on before displaying results, "
        "default %(default)s",
    )
    parser.add_argument(
        "--duration",
        default=30,
        type=int,
        help="How many seconds long the stream responses are plotting, "
        "default %(default)s",
    )
    parser.add_argument(
        "--server-url",
        default="http://localhost",
        help="The url to the server, probably in the format of "
        "http://IP_ADDRESS:PORT, default %(default)s",
    )
    parser.add_argument(
        "--out",
        default="brainframe_monitor.fps_history",
        help="FPS throughput history will be saved in an output file.",
    )
    parser.add_argument(
        "--no-screen",
        dest="no_screen",
        action="store_false",
        default=None,
        help="Use fake_screen to print instead of Python curses screen util",
    )
    parser.add_argument(
        "--version", action="store_true", help="Returns the version of the script"
    )

    args = subcommand_parse_args(parser)

    if args.version:
        print(version)
        exit(0)

    return args


if __name__ == "__main__":
    by_name["fps_monitor"]()
