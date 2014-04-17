#!/usr/bin/env python


# Copyright 2012,2013 Keith Fancher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse

from todotxt.indicator import TodoIndicator


def get_args():
    """Gets and parses command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--editor', action='store',
                        help='your favorite text editor')
    parser.add_argument('todo_filename', action='store',
                        help='your todo.txt file')
    return parser.parse_args()


def main():
    """My main() man."""
    args = get_args()
    ind = TodoIndicator(args.todo_filename, args.editor)
    ind.main()


if __name__ == "__main__":
    main()
