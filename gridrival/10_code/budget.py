import pandas as pd
import numpy as np

pd.set_option("mode.copy_on_write", True)

cars = pd.read_csv("../00_source_data/gridrival_salaries.csv")


cars[cars.Type == "driver"].sort_values("Salary", ascending=False)
cars[cars.Type == "team"].sort_values("Salary", ascending=False)

# cars.loc[cars.Driver == "Sainz", "contract"] = np.nan
cars.loc[cars.Driver == "Alonso", "contract"] = np.nan


cars.loc[cars.contract.notnull(), "Salary"].sum()
