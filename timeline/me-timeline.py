#!/usr/bin/env python3

# see https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/timeline.html

from datetime import datetime
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

with open('./me-timeline.json', 'r') as data_file:
    data = json.load(data_file)

dates = []
releases = []
features = []
for item in data:
    dates.append(item['year'])
    releases.append(item['release'])
    features.append(item['features'])
# Convert year (e.g. 2014) to datetime
dates = [datetime.strptime(d, "%Y") for d in dates]

# Choose some nice levels
levels = np.tile(
    [-2, 3, -1.5, 1.8, -.5, .5],
    int(np.ceil(len(dates)/6))
)[:len(dates)]

# Create figure and plot a stem plot with the date
fig, ax = plt.subplots(
    figsize=(10, 5),
    constrained_layout=True
)

markerline, stemline, baseline = ax.stem(
    dates,
    levels,
    linefmt="C3-",
    basefmt="-",
    use_line_collection=True # True for new behavior
)

plt.setp(markerline, mec="k", mfc="w", zorder=3)

# Shift the markers to the baseline by replacing the y-data by zeros.
markerline.set_ydata(np.zeros(len(dates)))

# annotate lines
vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
for d, l, r, f, va in zip(dates, levels, releases, features, vert):
    ax.annotate(
        r + (r and len(f)>0 and '\n' or '') + '\n'.join(f),
        xy=(d, l),
        xytext=(-3, np.sign(l)*3),
        textcoords="offset points",
        va=va,
        color="orange",
        bbox=dict(facecolor="#1a1a1a"),
        ha="center"
    )

# format xaxis with 1-year intervals
ax.get_xaxis().set_major_locator(mdates.YearLocator())
ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%Y"))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right", color="white")

# remove y axis and spines
ax.get_yaxis().set_visible(False)
for spine in ["left", "top", "right"]:
    ax.spines[spine].set_visible(False)

ax.margins(y=0.1)
# bbox_inches='tight' removes unnecessary whitespaces
plt.savefig(
    'me-timeline.png',
    bbox_inches='tight',
    edgecolor='green',
    facecolor='black',
    transparent=True
)
