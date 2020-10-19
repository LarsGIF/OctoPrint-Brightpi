import argparse
import math
import json
import os
import sys
from time import sleep

from brightpy.argparse_subparser_alias import AliasedSubParsersAction


BACKLIGHT_PATH = '/sys/class/backlight/intel_backlight'


class Backlight(object):
    def __init__(self):
        self.min = 1

        with open(os.path.join(BACKLIGHT_PATH, 'max_brightness')) as max_file:
            self.max = int(max_file.read())

        config_folder = os.path.join(
            os.environ.get(
                'XDG_CONFIG_HOME',
                os.path.join(
                    os.environ['HOME'],
                    '.config',
                )
            ),
            'BriPy',
        )

        self.config_path = config_path = os.path.join(
            config_folder,
            'config.json'
        )

        if not os.path.exists(config_folder):
            os.mkdir(config_folder)

        if not os.path.exists(config_path):
            self.config = {
                'ac': self.percentage,
                'battery': self.percentage,
            }

            self.write_config()
        else:
            with open(config_path) as config_file:
                self.config = json.load(config_file)

    def write_config(self):
        with open(self.config_path, 'w') as config_file:
            json.dump(self.config, config_file)

    @property
    def current(self):
        with open(os.path.join(BACKLIGHT_PATH, 'brightness')) as current_file:
            return int(current_file.read())

    @current.setter
    def current(self, value):
        if not (self.min <= value <= self.max):
            raise ValueError('Invalid value for backlight: %r' % value)

        with open(
            os.path.join(BACKLIGHT_PATH, 'brightness'),
            'w'
        ) as current_file:
            current_file.write('%d' % value)

    @property
    def percentage(self):
        return math.log(self.current) / math.log(self.max)

    @percentage.setter
    def percentage(self, value):
        if not (0 <= value <= 1):
            raise ValueError('Invalid percentage for backlight: %r' % value)

        self.current = math.exp(value * math.log(self.max))

    def change_percentage(self, amount, default_amount=None, time=200, steps=5):
        if amount is None:
            amount = default_amount

        percentage = self.percentage

        for step in range(steps):
            self.percentage = max(
                self.min / math.log(self.max),
                min(percentage + amount / 100 * (step + 1) / steps, 1),
            )
            sleep(time / steps / 1000.)

        if self.percentage == percentage:
            self.current = max(
                self.min,
                min(self.current + amount / abs(amount), self.max)
            )

    def increase(self, amount, **kwargs):
        self.change_percentage(amount, default_amount=5., **kwargs)

    def decrease(self, amount, **kwargs):
        self.change_percentage(
            -amount if amount else amount,
            default_amount=-5.,
            **kwargs
        )

    inc = increase
    dec = decrease

    def get(self, **kwargs):
        print(self.percentage * 100)

    def set(self, amount, **kwargs):
        self.change_percentage(
            amount - self.percentage * 100,
            **kwargs
        )

    def change_status(self, status, **kwargs):
        old_status = 'ac' if status == 'battery' else 'battery'

        self.config[old_status] = self.percentage
        self.write_config()

        percentage = self.percentage

        if self.config[status] == percentage:
            return

        self.change_percentage(
            (self.config[status] - percentage) * 100,
            **kwargs
        )


def ac():
    Backlight().change_status('ac')


def battery():
    Backlight().change_status('battery')


def main():
    parser = argparse.ArgumentParser(
        description='Control the backlight through sysfs',
    )
    parser.register('action', 'parsers', AliasedSubParsersAction)
    subparsers = parser.add_subparsers(dest='action')
    increase_parser = subparsers.add_parser(
        'increase',
        help='Increase backlight brightness',
        aliases=('inc', '+'),
    )
    decrease_parser = subparsers.add_parser(
        'decrease',
        help='Decrease backlight brightness',
        aliases=('dec', '-'),
    )

    for subparser, prefix in (
        (increase_parser, 'inc'),
        (decrease_parser, 'dec')
    ):
        subparser.add_argument(
            'amount',
            type=float,
            nargs='?',
            help='Percentage to {}rease brightness by'.format(prefix),
        )

    get_parser = subparsers.add_parser(
        'get',
        help='Get backlight brightness',
    )
    set_parser = subparsers.add_parser(
        'set',
        help='Set backlight brightness',
        aliases=('=',),
    )
    set_parser.add_argument(
        'amount',
        type=float,
        help='Percentage to set brightness to',
    )
    change_status_parser = subparsers.add_parser(
        'change_status',
        help='Change brightness based on power status (AC or battery)',
    )
    change_status_parser.add_argument(
        'status',
        choices=('ac', 'battery'),
        help='Current power status to set brightness to',
    )

    for subparser in (
        increase_parser,
        decrease_parser,
        set_parser,
        change_status_parser,
    ):
        subparser.add_argument(
            '-t',
            '--time',
            type=int,
            default=argparse.SUPPRESS,
            help='Length of time to spend fading the brightness',
        )
        subparser.add_argument(
            '-s',
            '--steps',
            type=int,
            default=argparse.SUPPRESS,
            help='Number of steps to take while fading the brightness',
        )

    args = parser.parse_args()

    backlight = Backlight()

    action = args.action
    del args.action

    if action in ('+', '-'):
        action = 'inc' if action == '+' else 'dec'
    elif action == '=':
        action = 'set'
    elif not action:
        action = 'get'

    getattr(backlight, action)(**vars(args))


if __name__ == '__main__':
    main()
