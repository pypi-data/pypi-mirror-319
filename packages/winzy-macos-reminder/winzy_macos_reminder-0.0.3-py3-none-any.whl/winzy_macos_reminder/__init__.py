import winzy
from dateutil.parser import parse
import subprocess


def create_reminder(description, date_str, date_format):
    try:
        # Parse the date string using dateutil's fuzzy logic
        if date_str is not None:
            parsed_date = parse(date_str, fuzzy=True)
            text_t = description
        else:
            parsed_date, text_t = parse(description, fuzzy_with_tokens=True)
            text_t = " ".join(text_t)

        # Combine the user-provided date format with the time format
        time_format = "%H:%M:%S"
        applescript_date = parsed_date.strftime(f"{date_format} {time_format}")

        # Prepare the AppleScript code
        applescript_code = f"""
        tell application "Reminders"
            set newReminder to make new reminder with properties {{name:"{text_t}"}}
            set remind me date of newReminder to date "{applescript_date}"
        end tell
        """

        # Run the AppleScript
        subprocess.run(["osascript", "-e", applescript_code], check=True)
        print(
            f'Reminder created: "{description}" on {parsed_date.strftime("%A, %B %d, %Y at %I:%M %p")}'
        )

    except Exception as e:
        print(f"Error: {e}")


def create_parser(subparser):
    parser = subparser.add_parser(
        "remind", description="Create reminders in macos with cli"
    )
    # Add subprser arguments here.
    parser.add_argument(
        "description", type=str, nargs="*", help="The description of the reminder."
    )
    parser.add_argument(
        "-dt",
        "--datetime",
        type=str,
        default=None,
        help="The date and time for the reminder (e.g., '16 December 10am').",
    )
    parser.add_argument(
        "-df",
        "--date-format",
        type=str,
        default="%d/%m/%Y",
        help="The expected date format (default: '%%d/%%m/%%Y').",
    )
    return parser


class WinzyPlugin:
    """ Create reminers in macos in cli """

    __name__ = "remind"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.run)

    def run(self, args):
        description = " ".join(args.description)
        create_reminder(description, args.datetime, args.date_format)

    def hello(self, args):
        # this routine will be called when "winzy remind is called."
        print("Hello! This is an example ``winzy`` plugin.")


remind_plugin = WinzyPlugin()
