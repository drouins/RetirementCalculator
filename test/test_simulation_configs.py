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
import os
import sys
import unittest

# Add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import data


class TestSimulationConfigs(unittest.TestCase):
    def setUp(self):
        self.default_configs = {'name': 'UNIT TEST',
                                'birthday': None,
                                'simulationStart': None,
                                'retirementAge': None,
                                'finalAge': None}

    def test_given_no_simulation_start_then_starts_with_current_year(self):
        current_year = datetime.datetime.now().year
        configs = data.SimulationConfigs(configs=self.default_configs)
        self.assertEqual(configs.first_year_of_simulation, current_year)

    def test_given_simulation_start_then_starts_with_provided_year(self):
        self.default_configs['simulationStart'] = 1942
        configs = data.SimulationConfigs(configs=self.default_configs)
        self.assertEqual(configs.first_year_of_simulation, 1942)

    def test_given_no_birthday_when_last_year_then_value_error(self):
        self.default_configs['finalAge'] = 100
        configs = data.SimulationConfigs(configs=self.default_configs)
        with self.assertRaises(ValueError):
            configs.last_year_of_simulation

    def test_given_invalid_birthday_when_last_year_then_value_error(self):
        self.default_configs['finalAge'] = 100
        self.default_configs['birthday'] = '195-06-21'
        configs = data.SimulationConfigs(configs=self.default_configs)
        with self.assertRaises(ValueError):
            configs.last_year_of_simulation

        self.default_configs['birthday'] = '1950-invalid'
        configs = data.SimulationConfigs(configs=self.default_configs)
        with self.assertRaises(ValueError):
            configs.last_year_of_simulation

        self.default_configs['birthday'] = '1950-august'
        configs = data.SimulationConfigs(configs=self.default_configs)
        with self.assertRaises(ValueError):
            configs.last_year_of_simulation

        self.default_configs['birthday'] = '1950-08'
        configs = data.SimulationConfigs(configs=self.default_configs)
        with self.assertRaises(ValueError):
            configs.last_year_of_simulation

        self.default_configs['birthday'] = '1950-08-60'
        configs = data.SimulationConfigs(configs=self.default_configs)
        with self.assertRaises(ValueError):
            configs.last_year_of_simulation

    def test_given_birth_year_when_last_year_then_valid(self):
        # Must work for integer value or string value
        self.default_configs['finalAge'] = 100
        self.default_configs['birthday'] = 1942
        configs = data.SimulationConfigs(configs=self.default_configs)
        self.assertEqual(configs.last_year_of_simulation, 2042)  # 1942 + 100

        self.default_configs['finalAge'] = 95
        self.default_configs['birthday'] = '1950'
        configs = data.SimulationConfigs(configs=self.default_configs)
        self.assertEqual(configs.last_year_of_simulation, 2045)  # 1950 + 95

    def test_given_birthday_when_last_year_then_valid(self):
        self.default_configs['finalAge'] = 100
        self.default_configs['birthday'] = '1950-06-21'
        configs = data.SimulationConfigs(configs=self.default_configs)
        self.assertEqual(configs.last_year_of_simulation, 2050)  # 1950 + 100
