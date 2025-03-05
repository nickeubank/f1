import numpy as np
import pandas as pd

BUDGET = 100

pd.set_option("mode.copy_on_write", True)
drivers = pd.read_csv("../00_source_data/gridrival_salaries.csv")

drivers["locked"] = drivers[drivers["contract"].notnull()]


def value_selections(selections):

    # checks
    if len(selections[selections["type"] == "team"] > 1):
        raise ValueError("Too many teams")
    if len(selections[selections["type"] == "team"] == 0):
        raise ValueError("No team")

    if len(selections[selections["type"] == "driver"] > 5):
        raise ValueError("Too many drivers")
    if len(selections[selections["type"] == "team"] < 5):
        raise ValueError("Too few drivers")

    # Star driver double
    star_able = selections[(selections["salary"] < 15), "score"].max().squeeze()
    assert (selections["score"] == star_able).sum() == 1
    selections.loc[selections.score == star_able, "score"] *= 2

    # check budget
    if selections.salary.sum() > BUDGET:
        raise ValueError(f"Over Budget. Totals: {selections.salary.sum()}")

    return selections.score.sum()
