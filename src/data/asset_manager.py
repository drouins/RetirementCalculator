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

from .assets import Assets
from .registered_retirement_savings import RegisteredRetirementSavings
from . import utils


class AssetManager(Assets):
    def __init__(self, input_directory, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not os.path.isdir(input_directory):
            raise ValueError(f'{input_directory} is not a valid directory.')

        # List all files in the directory and filter files that match the pattern expenses_*.json
        assets_files = [f for f in os.listdir(input_directory) if f.startswith('assets_') and f.endswith('.json')]

        self._assets = []

        for assets_file in assets_files:
            with open(os.path.join(input_directory, assets_file)) as file:
                assets_config = json.load(file)

                # Dynamically instantiate the class using globals()
                assets_class_name = assets_config['class']
                if assets_class_name not in globals():
                    raise ValueError(f'Unknown class name name \'{assets_class_name}\' specified in the config.')

                assets_cls = globals()[assets_class_name]
                self._assets.append(assets_cls(configs=assets_config))

    def get_value_for_year(self, year):
        if not self._assets:
            return 0
        return utils.as_cash_amount(sum([a.get_value_for_year(year) for a in self._assets]))

    def get_minimum_withdrawal_for_year(self, year):
        # TODO
        return 0
