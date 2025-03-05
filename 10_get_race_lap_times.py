import fastf1 as f1
import numpy as np
import pandas as pd

f1.Cache.enable_cache("fastf1_cache/")
events = f1.get_event_schedule(2022)

# Austria is round 11, so stop there
race_results = list()
quali_results = list()
for round in range(1, 12):
    # Races
    r = f1.get_session(2022, round, "Race")
    r.load()
    r = r.results
    r["round"] = round
    r["race_time"] = r.Time
    r = r.drop(["Q1", "Q2", "Q3", "BroadcastName", "FirstName"], axis="columns")
    race_results.append(r)

    # Quali
    q = f1.get_session(2022, round, "Qualifying")
    q.load()
    q = q.results
    q["round"] = round
    q["quali_position"] = q.Position
    q = q[["round", "FullName", "quali_position", "Q1", "Q2", "Q3"]]
    quali_results.append(q)

########
# Build Master Results DF
########

races = pd.concat(race_results)
qualis = pd.concat(quali_results)

results = pd.merge(
    races, qualis, on=["FullName", "round"], validate="1:1", how="outer", indicator=True
)

# Check mis-merge—Mick? weird, but ok.
results._merge.value_counts()
results[results._merge != "both"]
results = results.drop(columns=["_merge"])

####
# Get best quali time
####

quali_list = ["Q1", "Q2", "Q3"]


def get_seconds(x):
    if pd.isnull(x):
        return np.nan
    else:
        return np.float64(x.seconds)


for q in quali_list:
    # results[q] = results[q].apply(get_seconds).copy()
    results[q] = results[q].dt.seconds

results["quali_seconds"] = np.min(results[quali_list], axis=0)

# Convert times to speed as pct of fastest speed.

results["race_seconds"] = results.race_time.dt.seconds
results["race_pct_fastest"] = (
    results.groupby(["round"])["race_seconds"].transform(np.min)
    / results["race_seconds"]
)
