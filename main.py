# Import Meteostat library and dependencies
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily

# Set time period
start = datetime(2011, 1, 1)
end = datetime(2021, 12, 31)

# Create Point for Vancouver, BC
kharthoum = Point(15.508, 32.522, 381)

# Get daily data for 2018
data = Daily(kharthoum, start, end)
data = data.fetch()

# Plot line chart including average, minimum and maximum temperature
data.plot(y=['tavg', 'prcp', 'wspd'])
plt.show()