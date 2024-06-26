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
import collections
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

        def adjust_for_inflation(self, inflation_rate, years_in_future):
            adjusted_rates = TaxCalculator.TaxRanges()
            adjustment_coefficient = (1 + inflation_rate) ** years_in_future
            for income_range, rate in self._ranges:
                min_income, max_income = income_range
                adjusted_rates.add_range(adjustment_coefficient * min_income,
                                         adjustment_coefficient * max_income,
                                         rate)
            return adjusted_rates

        def add_range(self, min_income, max_income, rate):
            self._ranges.append(((min_income, max_income), rate))
            self._ranges = sorted(self._ranges, key=lambda x: x[0][0])  # Always sorted by min income in range

        def get_tax_amount(self, income):
            tax_amount = 0
            for income_range, rate in self._ranges:
                income_in_range = min(income_range[1], income)
                taxable_at_rate = max(0, income_in_range - income_range[0])
                tax_amount_at_rate = rate * taxable_at_rate
                tax_amount += tax_amount_at_rate
            return round(tax_amount, 2)

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

    @property
    def last_year(self):
        if not self._rates:
            return None
        return sorted(self._rates.keys())[-1]

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

    def get_rates_for_year(self, year=None):
        year = year or self.last_year
        if year in self._rates:
            rates = self._rates[year]
        elif year > self.last_year:
            ref_year = self.last_year
            rates = self._rates[ref_year].adjust_for_inflation(inflation_rate=self._inflation,
                                                               years_in_future=year-ref_year)
        else:
            raise NotImplemented
        return rates

    def get_tax_amount(self, income, year=None):
        rates = self.get_rates_for_year(year)
        return rates.get_tax_amount(income)

    def get_pretax_for_aftertax(self, income, year=None):
        rates = self.get_rates_for_year(year)

        # Iteratively converge to the answer
        pretax_income = collections.deque(maxlen=2)
        pretax_income.extend([0, income])
        while abs(pretax_income[-1] - pretax_income[-2]) > 0.01:
            estimated_taxes = rates.get_tax_amount(pretax_income[-1])
            pretax_income.append(income + estimated_taxes)

        return pretax_income[-1]
