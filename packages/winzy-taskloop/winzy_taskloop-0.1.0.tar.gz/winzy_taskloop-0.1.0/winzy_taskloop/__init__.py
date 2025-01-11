import winzy
import time
import subprocess
import signal
import sys
from datetime import datetime, timedelta


def parse_time(time_str):
    """Convert time string with units (s/m/h) to seconds"""
    unit = time_str[-1].lower()
    value = float(time_str[:-1])

    if unit == "s":
        return value
    elif unit == "m":
        return value * 60
    elif unit == "h":
        return value * 3600
    else:
        raise ValueError("Time must end with s, m, or h (e.g., 30s, 5m, 1h)")


def run_command(command):
    """Execute the given command"""
    try:
        subprocess.run(command, shell=True)
    except subprocess.SubprocessError as e:
        print(f"Error executing command: {e}")


def main(args):

    try:
        interval = parse_time(args.every)
        duration = parse_time(args.till)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration)

    def signal_handler(signum, frame):
        print("\nGracefully stopping the command runner...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print(f"Starting command runner at {start_time.strftime('%H:%M:%S')}")
    print(
        f"Will run '{args.run}' every {args.every} until {end_time.strftime('%H:%M:%S')}"
    )
    print("Press Ctrl+C to stop\n")

    try:
        while datetime.now() < end_time:
            run_command(args.run)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nGracefully stopping the command runner...")
        sys.exit(0)


def create_parser(subparser):
    parser = subparser.add_parser("taskloop", description="Run tasks in loop from cli")
    # Add subprser arguments here.
    parser.add_argument("run", help="Command to run")
    parser.add_argument(
        "-e", "--every", default="30s", help="Interval between runs (e.g., 30s, 5m, 1h)"
    )
    parser.add_argument(
        "-t", "--till", default="15m", help="Total duration to run (e.g., 30m, 1h)"
    )
    return parser


class WinzyPlugin:
    """ Run tasks in loop from cli """

    __name__ = "taskloop"

    @winzy.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        main(args)

    def hello(self, args):
        # this routine will be called when 'winzy taskloop' is called.
        print("Hello! This is an example ``winzy`` plugin.")


taskloop_plugin = WinzyPlugin()
