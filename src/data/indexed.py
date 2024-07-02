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

from . import utils


class Indexed:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'configs' in kwargs:
            configs = kwargs.get('configs')
            self._index_rate = utils.get_percentage(configs['indexRate'])
            self._reference_year = configs['referenceYear']
            self._reference_value = configs['value']
        else:
            raise ValueError("Missing 'configs' argument.")

    def get_indexed_value_for_year(self, year):
        years_in_future = year - self._reference_year
        return self._reference_value * (1 + self._index_rate) ** years_in_future
