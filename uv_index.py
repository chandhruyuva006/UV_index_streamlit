# import datetime
from datetime import datetime, timedelta, timezone
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st


def convert_to_local_time(dt_str):
	#convert the string to datetime object 'Z' means UTC
	dt_utc = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

	# to pass into the timezone calc
	offset = timezone(timedelta(hours=5, minutes=30))

	# adds 5:30 to UTC GMT+5:30
	dt_gmt_530 = dt_utc.astimezone(offset)

	return dt_gmt_530

CITY = 'Chennai'

lat = '13.0843'  #Chennai's longitude and latitude
lon = '80.2705'

url = f'https://currentuvindex.com/api/v1/uvi?latitude={lat}&longitude={lon}'

response= requests.get(url).json()

forecast = response['forecast']  # It is a list of dicts [{'time': str, 'uvi': float}]

times = [convert_to_local_time(entry['time']) for entry in forecast]
uvi_values = [entry['uvi'] for entry in forecast]


# --- Plot ---
fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.bar(times, uvi_values, color='#f272ca', width=0.03)


ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b, %H:%M'))
plt.xticks(rotation=45, ha='right')
plt.xlabel("Local Date & Time (GMT+5:30)")
plt.ylabel("UV Index")
plt.title(f"UV Index Forecast ({CITY})", fontsize=14, weight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Add guideline lines
uvi_levels = [
    (3, 'Moderate (3)', 'green'),
    (6, 'High (6)', 'orange'),
    (8, 'Very High (8)', 'red'),
    (11, 'Extreme (11)', 'purple'),
]
for level, label, color in uvi_levels:
    ax.axhline(y=level, color=color, linestyle='--', linewidth=1)
    ax.text(times[0], level + 0.1, label, color=color, fontsize=9, verticalalignment='bottom')

plt.tight_layout()

# --- Show in Streamlit ---

st.header(f"\u263c Real-time UV Index Forecast - {CITY}")
st.pyplot(fig)

