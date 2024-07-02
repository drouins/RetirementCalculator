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

from .expenses import Expenses
from .indexed_expenses import IndexedExpenses


class ExpensesManager(Expenses):
    def __init__(self, input_directory):
        if not os.path.isdir(input_directory):
            raise ValueError(f"{input_directory} is not a valid directory.")

        # List all files in the directory and filter files that match the pattern expenses_*.json
        expenses_files = [f for f in os.listdir(input_directory) if f.startswith('expenses_') and f.endswith('.json')]

        self._expenses = []

        for expenses_file in expenses_files:
            with open(os.path.join(input_directory, expenses_file)) as file:
                expenses_config = json.load(file)

                # Dynamically instantiate the class using globals()
                expenses_class_name = expenses_config['class']
                if expenses_class_name not in globals():
                    raise ValueError(f'Unknown class name name \'{expenses_class_name}\' specified in the config.')

                expenses_cls = globals()[expenses_class_name]
                self._expenses.append(expenses_cls(configs=expenses_config))

    def get_expenses_for_year(self, year):
        if not self._expenses:
            return 0

        return sum([e.get_expenses_for_year(year) for e in self._expenses])
