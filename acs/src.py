#!/usr/bin/env python3

from pygris.data import get_census
import pandas as pd

# dataset: acs/acs1/subject
#   variable: Total Households => S1101_C01_001E
# source: https://api.census.gov/data/2021/acs/acs1/subject/variables.html
#
# geoid:
#   STATEFP: NY => 36
#   COUNTYFP: Queens => 081
# source: https://www.census.gov/library/reference/code-lists/ansi.html#cou

census_vars = {
    "S1101_C01_001E": "TOTAL_HOUSEHOLDS"
}

ACS1_START_YEAR = 2015
ACS1_END_YEAR = 2023
ACS1_SKIP_YEARS = [2020] # no data for 2020, maybe use try-catch instead?
years = [year
         for year in range(ACS1_START_YEAR, ACS1_END_YEAR + 1)
         if year not in ACS1_SKIP_YEARS]


df_queens_households = None

for aYear in years:
    _df = get_census(dataset = "acs/acs1/subject",
                            variables = ["NAME", "S1101_C01_001E"],
                            year = aYear,
                            params = {
                                "for": "county:081",
                                "in": "state:36"
                            },
                            return_geoid = True,
                            guess_dtypes = True)

    _df['YEAR'] = aYear

    if df_queens_households is None:
        df_queens_households = _df
    else:
        df_queens_households = pd.concat([df_queens_households, _df])

df_queens_households.rename(columns = census_vars, inplace=True)
df_queens_households
