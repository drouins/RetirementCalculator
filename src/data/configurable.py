#     Retirement Calculator, a canadian retirement simulator
#     Copyright (C) 2024  Stephane Drouin
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import os


class Configurable:
    def __init__(self, config_filename, input_directory=None, configs=None):
        if input_directory:
            with open(os.path.join(input_directory, config_filename)) as file:
                self._configs = json.load(file)
        else:
            self._configs = configs

    @property
    def configs(self):
        return self._configs
