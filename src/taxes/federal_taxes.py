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
import re

from .tax_calculator import TaxCalculator


class FederalTaxes(TaxCalculator):
    def __init__(self, cache_config=None, bracket_url=None, **kwargs):
        cache_config = cache_config or 'federal_taxes.json'
        bracket_url = bracket_url or 'https://www.canada.ca/api/assets/cra-arc/content-fragments/income-tax-rates.json'
        super().__init__(cache_config=cache_config,
                         bracket_url=bracket_url,
                         **kwargs)

    def parse_bracket_url(self, data):
        data = json.loads(data)
        data = data['properties']['elements']['federalRates']
        available_years = data['variationsOrder']

        for year in available_years:
            tax_data = data['variations'][year]['value']
            # This data is a HTML table that requires more parsing
            tax_data = tax_data.split('<td>')
            # First index will be headers and stuff
            # Then afterwards it will alternate between a tax rate (float with the % sign) and
            # a amount range in text format
            tax_data = tax_data[1:]
            tax_data = [(tax_data[i], tax_data[i + 1]) for i in range(0, len(tax_data), 2)]

            tax_ranges = TaxCalculator.TaxRanges()
            for tax_rate, income_range in tax_data:
                tax_rate = FederalTaxes._get_percentage(tax_rate)
                income_range = FederalTaxes.extract_amounts(income_range)
                tax_ranges.add_range(min_income=income_range[0],
                                     max_income=income_range[1],
                                     rate=tax_rate)
            self.add_tax_ranges(year=int(year), tax_ranges=tax_ranges)

    @staticmethod
    def _get_percentage(text):
        percentage = re.findall(r'(\d+\.?\d+?%)', text)[0]
        return float(percentage.replace(r'%', '')) / 100

    @staticmethod
    def extract_amounts(text):
        # Use regex to find all numeric values in the string
        amounts = re.findall(r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)', text)

        # Convert the extracted values to integers, removing any commas
        amounts = [float(amount.replace(',', '')) for amount in amounts]

        # Case with first or last bracket
        if len(amounts) == 1:
            if 'or less' in text:
                amounts = [0, amounts[0]]
            else:
                amounts = [amounts[0], float('inf')]

        return amounts
