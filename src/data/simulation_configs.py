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

import datetime
import json
import os


class SimulationConfigs:
    def __init__(self, input_directory=None, configs=None):
        if input_directory:
            with open(os.path.join(input_directory, 'config.json')) as file:
                self._configs = json.load(file)
        else:
            self._configs = configs

    @property
    def first_year_of_simulation(self):
        if 'simulationStart' not in self._configs or not self._configs['simulationStart']:
            return datetime.datetime.now().year
        return int(self._configs['simulationStart'])

    @property
    def birth_year(self):
        if 'birthday' not in self._configs or not self._configs['birthday']:
            raise ValueError('No birthday provided.')

        # Check if the string is just a year
        if isinstance(self._configs['birthday'], int):
            return self._configs['birthday']

        if len(self._configs['birthday']) == 4 and self._configs['birthday'].isdigit():
            return int(self._configs['birthday'])

        # Try to parse the full date
        date_obj = datetime.datetime.strptime(self._configs['birthday'], '%Y-%m-%d')
        return date_obj.year

    @property
    def last_year_of_simulation(self):
        return self.birth_year + self._configs['finalAge']
