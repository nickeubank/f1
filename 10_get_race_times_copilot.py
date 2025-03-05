import fastf1
import pandas as pd

# Define the races to loop over
races = [
    ('Bahrain', 'R'),
    ('Imola', 'R'),
    ('Portugal', 'R'),
    ('Spain', 'R'),
    ('Monaco', 'R'),
    ('Azerbaijan', 'R'),
    ('France', 'R'),
    ('Styria', 'R'),
    ('Austria', 'R'),
    ('Great Britain', 'R'),
    ('Hungary', 'R'),
    ('Belgium', 'R'),
    ('Netherlands', 'R'),
    ('Italy', 'R'),
    ('Russia', 'R'),
    ('Turkey', 'R'),
    ('United States', 'R'),
    ('Mexico', 'R'),
    ('Brazil', 'R'),
    ('Saudi Arabia', 'R'),
    ('Abu Dhabi', 'R')
]

# Loop over the races and calculate the total race time for each driver
results = []
for race in races:
    # Load the session data for the race
    session = fastf1.get_session(2021, race[0], race[1])

    # Get the lap times for each driver
    lap_times = session.load_laps(with_telemetry=True)

    # Calculate the total race time for each driver
    race_times = {}
    for driver in lap_times:
        race_time = sum(lap_times[driver]['LapTime'])
        race_times[driver] = race_time

    # Add the results to the list
    results.append(race_times)

# Create a Pandas DataFrame from the results
df = pd.DataFrame(results, index=[race[0] for race in races])

# Print the DataFrame
print(df)