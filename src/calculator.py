#! /usr/local/bin/python3 -u
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

import argparse

import data
import taxes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_directory', default='data', help='Input data directory.')
    options = parser.parse_args()

    expenses = data.ExpensesManager(input_directory=options.input_directory)
    assets = data.AssetManager(input_directory=options.input_directory)
    simulation_configs = data.SimulationConfigs(input_directory=options.input_directory)
    print(f'Simulating from {simulation_configs.first_year_of_simulation} until '
          f'{simulation_configs.last_year_of_simulation}.')
    for year in range(simulation_configs.first_year_of_simulation, simulation_configs.last_year_of_simulation):
        print(f'{year}: Expenses={expenses.get_expenses_for_year(year)}{simulation_configs.money_symbol}, '
              f'Assets={assets.get_value_for_year(year)}{simulation_configs.money_symbol}')

    #federal_taxes = taxes.FederalTaxes()


if __name__ == '__main__':
    main()
