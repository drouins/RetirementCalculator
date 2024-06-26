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

import abc
import json
import os
import urllib.request


class TaxCalculator(abc.ABC):
    class TaxRanges:
        def __init__(self):
            self._ranges = []

        def __repr__(self):
            return str(self._ranges)

        def __json__(self):
            return self._ranges

        def add_range(self, min_income, max_income, rate):
            self._ranges.append(((min_income, max_income), rate))
            self._ranges = sorted(self._ranges, key=lambda x: x[0][0])  # Always sorted by min income in range

    class TaxRangesEncoder(json.JSONEncoder):
        def default(self, obj):
            if hasattr(obj, '__json__'):
                return obj.__json__()
            return super().default(obj)

    def __init__(self, cache_config, bracket_config=None, bracket_url=None, inflation=0):
        cache_config = TaxCalculator._get_cache_filename(cache_config)
        self._inflation = inflation
        self._rates = {}

        # When bracket_config is specified, will load that data and be done with it.
        if bracket_config:
            self._load_config(bracket_config)
        # Otherwise, when bracket_url is specified, will fetch that data and attempt to parse it:
        # - when successful, will export it to default_config
        # - when not successful, will try to load cache_config
        elif bracket_url:
            try:
                with urllib.request.urlopen(bracket_url) as url:
                    self.parse_bracket_url(url.read().decode())
            except Exception as ex:
                pass
            else:
                if cache_config:
                    print('Exporting TaxRanges to cache file')
                    try:
                        with open(TaxCalculator._get_cache_filename(cache_config), 'w') as file:
                            json.dump(self._rates, file, cls=TaxCalculator.TaxRangesEncoder, indent=4)
                    except:
                        pass

        # When everything else fails, will raise exception
        if not self._rates and cache_config:
            print('Loading TaxRanges from cache file')
            try:
                cache_config = TaxCalculator._get_cache_filename(cache_config)
                self._load_config(cache_config)
            except:
                self._rates.clear()

        if not self._rates:
            raise ValueError('Unable to get tax range data.')

    @abc.abstractmethod
    def parse_bracket_url(self, data):
        raise NotImplemented

    def add_tax_ranges(self, year: int, tax_ranges: TaxRanges):
        self._rates[year] = tax_ranges

    @staticmethod
    def _get_cache_filename(cache_config):
        if not isinstance(cache_config, str):
            return None
        cache_path = os.path.join('.', 'cache')
        if not os.path.isdir(cache_path):
            os.makedirs(cache_path)
        return os.path.join(cache_path, cache_config)

    def _load_config(self, config_filename):
        if os.path.isfile(config_filename):
            with open(config_filename, 'r') as file:
                loaded_data = json.load(file)
            print(loaded_data)

    def get_tax_amount(self, income, year=None):
        raise NotImplemented

    def get_pretax_for_aftertax(self, income, year=None):
        raise NotImplemented
