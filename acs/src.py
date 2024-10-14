#!/usr/bin/env python3

from pygris.data import get_census
import matplotlib.pyplot as plt
import pandas as pd
import re

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
                                "for": "public use microdata area:*",
                                "in": "state:36"
                            },
                            return_geoid = True,
                            guess_dtypes = True)

    _df['YEAR'] = aYear

    if df_queens_households is None:
        df_queens_households = _df
    else:
        df_queens_households = pd.concat([df_queens_households, _df])

# rename variable to human-readable label
df_queens_households.rename(columns = census_vars, inplace=True)
# filter only to Queens districts
queens_districts_households = df_queens_households[df_queens_households['NAME'].str.startswith('NYC-Queens')]
# create QN{#} district id column
queens_districts_households['DISTRICT'] = 'QN' + queens_districts_households['NAME'].str.extract(r'(\d+)')

out_df = queens_districts_households[['DISTRICT', 'YEAR', 'TOTAL_HOUSEHOLDS']]
# out_df.to_csv('queens_housholds_2015_2023')

# quick review
# queens_households = queens_districts_households[queens_districts_households['DISTRICT'].isin(['QN5','QN10'])]
# queens_hh_by_year = queens_households[['YEAR','TOTAL_HOUSEHOLDS']].groupby('YEAR').sum()
# households = queens_hh_by_year['TOTAL_HOUSEHOLDS']
#
# plt.figure(figsize=(9,3))
# plt.bar(years, households)
# plt.suptitle('Queens, NY Curbside organics, 2015-2023')
# plt.show()
