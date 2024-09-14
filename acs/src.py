#!/usr/bin/env python3

from pygris.data import get_census

# geoid:
#   STATEFP: NY => 36
#   COUNTYFP: Queens => 081
# source: https://www.census.gov/library/reference/code-lists/ansi.html#cou

# example from to get a feel for this package
us_youth_sahie = get_census(dataset = "timeseries/healthins/sahie",
                            variables = "PCTUI_PT",
                            params = {
                                "for": "county:081",
                                "in": "state:36",
                                "time": 2019,
                                "AGECAT": 4
                            },
                            return_geoid = True,
                            guess_dtypes = True)
