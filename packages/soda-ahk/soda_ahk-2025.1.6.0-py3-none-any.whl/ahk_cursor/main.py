import argparse
from ahk_cursor.stop import main as stop
from ahk_cursor.move_cursor import main as move_cursor

parser = argparse.ArgumentParser()

parser.add_argument(
    "--stop", action="store_true", default=False, help="Stop the script if it's running"
)

def main():
    args = parser.parse_args()

    if args.stop:
        stop()
    else:
        move_cursor()
