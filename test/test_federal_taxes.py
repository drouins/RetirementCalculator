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
import sys
import unittest
import unittest.mock
from urllib.error import HTTPError, URLError

# Add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import taxes


class TestFederalTaxes(unittest.TestCase):
    @property
    def valid_mock_response(self):
        # Mock data structure in Python dictionary format
        mock_data = {
            'properties': {
                'elements': {
                    'federalRates': {
                        'variationsOrder': ['2023', '2024'],
                        'variations': {
                            "2023": {
                                "value": "<table class=\"table table-condensed\">\n    <caption>\n        Federal income tax rates for 2023\n    <\/caption>\n    <thead>\n        <tr>\n            <th scope=\"col\">Tax rate<\/th>\n            <th scope=\"col\">Taxable income threshold<\/th>\n        <\/tr>\n    <\/thead>\n    <tbody>\n        <tr>\n            <td>15%<\/td>\n            <td>on the portion of taxable income that is $53,359 or less, <strong>plus<\/strong><\/td>\n        <\/tr>\n        <tr>\n            <td>20.5%<\/td>\n            <td>on the portion of taxable income over $53,359 up to $106,717, <strong>plus<\/strong><\/td>\n        <\/tr>\n        <tr>\n            <td>26% <\/td>\n            <td>on the portion of taxable income over $106,717 up to $165,430, <strong>plus<\/strong><\/td>\n        <\/tr>\n        <tr>\n            <td>29%<\/td>\n            <td>on the portion of taxable income over $165,430 up to $235,675, <strong>plus<\/strong><\/td>\n        <\/tr>\n        <tr>\n            <td>33%<\/td>\n            <td>on the portion of taxable income over $235,675<\/td>\n        <\/tr>\n    <\/tbody>\n<\/table>"
                            },
                            '2024': {
                                'value': "<table class=\"table table-condensed\">\n    <caption>\n        Federal income tax rates for 2024\n    <\/caption>\n    <thead>\n        <tr>\n            <th scope=\"col\">Tax rate<\/th>\n            <th scope=\"col\">Taxable income threshold<\/th>\n        <\/tr>\n    <\/thead>\n    <tbody>\n        <tr>\n            <td>15%<\/td>\n            <td>on the portion of taxable income that is $55,867 or less, <strong>plus<\/strong><\/td>\n        <\/tr>\n        <tr>\n            <td>20.5%<\/td>\n            <td>on the portion of taxable income over $55,867 up to $111,733, <strong>plus<\/strong><\/td>\n        <\/tr>\n        <tr>\n            <td>26% <\/td>\n            <td>on the portion of taxable income over $111,733 up to $173,205, <strong>plus<\/strong><\/td>\n        <\/tr>\n        <tr>\n            <td>29%<\/td>\n            <td>on the portion of taxable income over $173,205 up to $246,752, <strong>plus<\/strong><\/td>\n        <\/tr>\n        <tr>\n            <td>33%<\/td>\n            <td>on the portion of taxable income over $246,752<\/td>\n        <\/tr>\n    <\/tbody>\n<\/table>"
                            }
                        }
                    }
                }
            }
        }
        mock_response = unittest.mock.MagicMock()
        mock_response.read.return_value = json.dumps(mock_data).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        return mock_response

    @property
    def invalid_mock_response(self):
        mock_response = unittest.mock.MagicMock()
        mock_response.read.return_value = b'some invalid json'
        mock_response.__enter__.return_value = mock_response
        return mock_response

    @unittest.mock.patch('urllib.request.urlopen')
    def test_given_valid_data_when_init_then_parses_correctly(self, mock_urlopen):
        mock_urlopen.return_value = self.valid_mock_response

        ft = taxes.FederalTaxes(cache_config=(1,))
        self.assertTrue(ft._rates)
        self.assertIn(2023, ft._rates)
        self.assertIn(2024, ft._rates)

    @unittest.mock.patch('urllib.request.urlopen')
    def test_given_valid_data_when_last_year_then_returns_last_year(self, mock_urlopen):
        mock_urlopen.return_value = self.valid_mock_response
        ft = taxes.FederalTaxes(cache_config=(1,))
        self.assertEqual(ft.last_year, 2024)

    @unittest.mock.patch('urllib.request.urlopen')
    def test_given_valid_data_when_get_tax_amount_then_returns_valid_amount(self, mock_urlopen):
        mock_urlopen.return_value = self.valid_mock_response
        # 2023 Federal taxes simulated with
        # https://ca.icalculator.com/income-tax-calculator/2023.html
        ft = taxes.FederalTaxes(cache_config=(1,))

        self.assertEqual(ft.get_tax_amount(30000, year=2023), 4500)
        self.assertEqual(ft.get_tax_amount(60000, year=2023), 9365.25)
        self.assertEqual(ft.get_tax_amount(90000, year=2023), 15515.25)
        self.assertEqual(ft.get_tax_amount(130000, year=2023), 24995.82)
        # Calculator returns 85930.69 with 29.33% instead of 29%
        self.assertEqual(ft.get_tax_amount(330000, year=2023), 85705.92)

    @unittest.mock.patch('urllib.request.urlopen')
    def test_given_valid_data_when_get_pretax_for_aftertax_then_returns_valid_amount(self, mock_urlopen):
        mock_urlopen.return_value = self.valid_mock_response
        ft = taxes.FederalTaxes(cache_config=(1,))

        # Using inverted values from test_given_valid_data_when_get_tax_amount_then_returns_valid_amount
        self.assertEqual(ft.get_pretax_for_aftertax(30000-4500, year=2023), 30000)
        self.assertEqual(ft.get_pretax_for_aftertax(60000-9365.25, year=2023), 60000)
        self.assertEqual(ft.get_pretax_for_aftertax(90000-15515.25, year=2023), 90000)
        self.assertEqual(ft.get_pretax_for_aftertax(130000-24995.82, year=2023), 130000)
        self.assertEqual(ft.get_pretax_for_aftertax(330000-85705.92, year=2023), 330000)

    @unittest.mock.patch('urllib.request.urlopen')
    def test_given_valid_data_when_get_tax_amount_then_returns_valid_amount_inflation_adjusted(self, mock_urlopen):
        mock_urlopen.return_value = self.valid_mock_response
        # 2023 Federal taxes simulated with
        # https://ca.icalculator.com/income-tax-calculator/2023.html
        ft = taxes.FederalTaxes(cache_config=(1,), inflation=0.025)

        self.assertEqual(ft.get_tax_amount(30000, year=2026), 4500)
        self.assertEqual(ft.get_tax_amount(60000, year=2026), 9071.76)
        self.assertEqual(ft.get_tax_amount(90000, year=2026), 15221.76)
        self.assertEqual(ft.get_tax_amount(130000, year=2026), 24115.34)
        self.assertEqual(ft.get_tax_amount(330000, year=2026), 83386.38)

    @unittest.mock.patch('urllib.request.urlopen')
    def test_given_invalid_data_when_init_then_raises_value_error(self, mock_urlopen):
        mock_urlopen.return_value = self.invalid_mock_response

        with self.assertRaises(ValueError):
            taxes.FederalTaxes(cache_config=(1,))

    @unittest.mock.patch('urllib.request.urlopen')
    def test_given_invalid_endpoint_when_init_then_raises_value_error(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError('http://example.com', 404, 'Not Found', None, None)
        with self.assertRaises(ValueError):
            taxes.FederalTaxes(cache_config=(1,))

    @unittest.mock.patch('urllib.request.urlopen')
    def test_given_invalid_url_when_init_then_raises_value_error(self, mock_urlopen):
        mock_urlopen.side_effect = URLError('Invalid URL')
        with self.assertRaises(ValueError):
            taxes.FederalTaxes(cache_config=(1,))
