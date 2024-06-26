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
    #def test_calculate_tax(self):
    #    self.assertEqual(self.calculator.calculate_tax(100, 0.2), 20)
    #    self.assertEqual(self.calculator.calculate_tax(200, 0.15), 30)
    #    self.assertEqual(self.calculator.calculate_tax(0, 0.2), 0)

    #def test_calculate_tax_with_zero_rate(self):
    #    self.assertEqual(self.calculator.calculate_tax(100, 0), 0)

    @property
    def valid_mock_data(self):
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
        return json.dumps(mock_data).encode('utf-8')

    @unittest.mock.patch('urllib.request.urlopen')
    def test_given_valid_data_when_init_then_parses_correctly(self, mock_urlopen):
        # Mock response object
        mock_response = unittest.mock.MagicMock()
        mock_response.read.return_value = self.valid_mock_data
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        ft = taxes.FederalTaxes(cache_config=(1,))
        self.assertTrue(ft._rates)
        self.assertIn(2023, ft._rates)
        self.assertIn(2024, ft._rates)

    @unittest.mock.patch('urllib.request.urlopen')
    def test_given_invalid_data_when_init_then_raises_value_error(self, mock_urlopen):
        # Mock response object
        mock_response = unittest.mock.MagicMock()
        mock_response.read.return_value = b'some invalid json'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

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
