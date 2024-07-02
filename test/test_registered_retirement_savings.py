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

import os
import sys
import unittest

# Add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from data.registered_retirement_savings import RegisteredRetirementSavings


class TestRegisteredRetirementSavings(unittest.TestCase):
    def setUp(self):
        self.default_configs = {'name': 'UNIT TEST',
                                'class': 'RegisteredRetirementSavings',
                                'value': 100,
                                'referenceYear': 2024,
                                'indexRate': '1%'}

    def test_given_one_year_in_past_when_get_value_for_year_then_returns_indexed(self):
        expenses = RegisteredRetirementSavings(configs=self.default_configs)
        self.assertEqual(expenses.get_value_for_year(2023), 99.01)

    def test_given_current_when_get_value_for_year_then_returns_reference(self):
        expenses = RegisteredRetirementSavings(configs=self.default_configs)
        self.assertEqual(expenses.get_value_for_year(2024), 100)

    def test_given_one_year_in_future_when_get_value_for_year_then_returns_indexed(self):
        expenses = RegisteredRetirementSavings(configs=self.default_configs)
        self.assertEqual(expenses.get_value_for_year(2025), 101)

    def test_given_two_year_in_future_when_get_value_for_year_then_returns_indexed(self):
        expenses = RegisteredRetirementSavings(configs=self.default_configs)
        self.assertEqual(expenses.get_value_for_year(2026), 102.01)
