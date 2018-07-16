"""
    vehicular: a CLI application to search craigslist for vehicles.
    Copyright (C) 2018 Alexander Potts
    See LICENSE.txt for full license.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
from vehicular.main import Run


def launch():
    """
    Launch script.
    """
    with Run() as run:
        if not run.credentials:
            print('This looks to be your first time running the progam: set '
                  'your credentials first.')
            run.do_credentials()
        run.cmdloop()


if __name__ == '__main__':
    launch()
