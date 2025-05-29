import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import webbrowser
from pytrends.request import TrendReq

# Set up Pytrends
pytrend = TrendReq(hl='en-US', tz=360)
keyword = "News"

# Interest by region
pytrend.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')
region_data = pytrend.interest_by_region()
region_data = region_data.sort_values(by=keyword, ascending=False).head(15)

# Country-wise interest barplot
plt.figure(figsize=(10, 6))
sns.barplot(x=region_data[keyword], y=region_data.index, palette="Blues_d")
plt.title(f"Top countries searching for '{keyword}'")
plt.xlabel("Interest")
plt.ylabel("Country")
plt.tight_layout()
plt.show()

# Choropleth world map using Plotly (saved and opened in browser)
region_data = region_data.reset_index()
fig = px.choropleth(region_data,
                    locations='geoName',
                    color=keyword,
                    title=f"Search interest for '{keyword}' by country",
                    color_continuous_scale='Blues')
fig.write_html("plotly_map.html")
webbrowser.open("plotly_map.html")

# Time-wise interest
time_df = pytrend.interest_over_time()

plt.figure(figsize=(12, 6))
plt.plot(time_df.index, time_df[keyword], marker='o', color='purple')
plt.title(f"Interest over time for '{keyword}'")
plt.xlabel("Date")
plt.ylabel("Interest")
plt.grid(True)
plt.tight_layout()
plt.show()

# Multiple keyword comparison
kw_list = ["cloud computing", "data science", "machine learning"]
pytrend.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='')

compare_df = pytrend.interest_over_time()

plt.figure(figsize=(12, 6))
for kw in kw_list:
    plt.plot(compare_df.index, compare_df[kw], marker='o', label=kw)

plt.title("Keyword comparison over time")
plt.xlabel("Date")
plt.ylabel("Interest")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
