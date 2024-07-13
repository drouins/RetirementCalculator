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

from .configurable import Configurable


class SimulationConfigs(Configurable):
    def __init__(self, input_directory=None, configs=None):
        super().__init__(config_filename='config.json', input_directory=input_directory, configs=configs)

    @property
    def first_year_of_simulation(self):
        if 'simulationStart' not in self.configs or not self.configs['simulationStart']:
            return datetime.datetime.now().year
        return int(self.configs['simulationStart'])

    @property
    def birth_year(self):
        if 'birthday' not in self.configs or not self.configs['birthday']:
            raise ValueError('No birthday provided.')

        # Check if the string is just a year
        if isinstance(self.configs['birthday'], int):
            return self.configs['birthday']

        if len(self.configs['birthday']) == 4 and self.configs['birthday'].isdigit():
            return int(self.configs['birthday'])

        # Try to parse the full date
        date_obj = datetime.datetime.strptime(self.configs['birthday'], '%Y-%m-%d')
        return date_obj.year

    @property
    def last_year_of_simulation(self):
        return self.birth_year + self.configs['finalAge']

    @property
    def money_symbol(self):
        return self.configs['moneySymbol']
