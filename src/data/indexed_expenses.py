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

from .configurable import Configurable
from .expenses import Expenses
from .indexed import Indexed
from . import utils


class IndexedExpenses(Expenses, Indexed, Configurable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, config_filename=None, **kwargs)

    def get_expenses_for_year(self, year):
        return utils.as_cash_amount(self.get_indexed_value_for_year(year))
