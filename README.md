# RetirementCalculator

# Modules

## `taxes`

The base class `TaxCalculator` represents the taxes, with `get_tax_amount`,
which estimates taxes for a given amount in some given year
and `get_pretax_for_after_tax`, which estimates how much pretax income is
required to produce some after tax income in some given year.

I am assuming some website will provide tax brackets so derived classes should implement
`parse_bracket_url`. I am also assuming that said website will provide bracket amounts
for a specific year, and calculations will make sure to index these brackets through the years.

Of course actual amounts will differ as taxes is a most complicated subject. In any
case, we will at least try to ballpark the amounts in the simulations.

## Executing the server

```bash
cd RCalculator
python manage.py runserver
```

Open your browser and visit http://127.0.0.1:8000 to load the application.

## Executing `unit tests`

From the root of the project:

```bash
python3 -m unittest
```
