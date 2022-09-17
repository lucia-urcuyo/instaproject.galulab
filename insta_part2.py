# Instagram project part 2: Analysis on data pulled from part 1
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import plotly.express as px

# Import files created in part 1
reels_data = pd.read_csv("Reels_Data.csv")
photos_data = pd.read_csv("Photos_Data.csv")

# Create an index column because for some reason pycharm doesn't understand when we call it
index = []
count = 0
for i in reels_data['id']:
        index.append(count)
        count = count + 1

reels_data.insert(0, 'index', index)

# Create a column that measures the enjoyment: the percentage of viewers that liked the video
reels_data['enjoyment'] = (reels_data['likes']/reels_data['plays']) * 100

# Create a shortened version of the caption columns to make it fit better in the tooltip of the graphs below
reels_data['shortcap'] = reels_data['caption'].str[:25]

# Bar plots for all variables

likesplot = px.bar(reels_data, x="index", y="likes", color="day_of_week", title="Likes", hover_data=['shortcap', 'hour posted', 'hashtags'])

# likesplot.show()

enjoyplot = px.bar(reels_data, x="index", y="enjoyment", color="day_of_week", title="Enjoyment", hover_data=['shortcap', 'hour posted', 'hashtags'])

# enjoyplot.show()

playsplot = px.bar(reels_data, x="index", y="plays", color="day_of_week", title="Plays", hover_data=['shortcap','hour posted', 'hashtags'])

# playsplot.show()

commentsplot = px.bar(reels_data, x="index", y="enjoyment", color="day_of_week", title="Comments", hover_data=['shortcap', 'hour posted', 'hashtags'])

# commentsplot.show()

# count how many reels where posted on each day of the week
postsperday = reels_data.groupby('day_of_week')['index'].count()

# convert pandas series to dataframes
postdailycount = postsperday.to_frame()

# Set index as new column (day_of_week)
postdailycount.reset_index(inplace=True)

# rename 'index' column to 'dailycount'
postdailycount.rename({'index': 'dailycount'}, axis=1, inplace=True)

# set 'dailycount' column as a variable
dailycount = postdailycount['dailycount']

# get the play counts for each day separately, not using this yet
saturdayposts = postdailycount.loc[postdailycount['day_of_week'] == 'Sat']

# get daily average plays
avgdailyplays = reels_data.groupby('day_of_week')['plays'].mean()

# convert pandas series to dataframes
dailyplaysmean = avgdailyplays.to_frame()

# Set index as new column (day_of_week)
dailyplaysmean.reset_index(inplace=True)

# add daily count as a new column
dailyplaysmean['dailycount'] = dailycount

# Make a bar plots of average plays per day
dailyplaysplot = px.bar(dailyplaysmean, x="day_of_week", y="plays", title='Average Daily Plays', hover_data=['dailycount'])
# dailyplaysplot.show()

# Extract data from each day of the week separately
sunday = reels_data.loc[reels_data['day_of_week'] == 'Sun']
monday = reels_data.loc[reels_data['day_of_week'] == 'Mon']
tuesday = reels_data.loc[reels_data['day_of_week'] == 'Tues']
wednesday = reels_data.loc[reels_data['day_of_week'] == 'Weds']
thursday = reels_data.loc[reels_data['day_of_week'] == 'Thurs']
friday = reels_data.loc[reels_data['day_of_week'] == 'Fri']
saturday = reels_data.loc[reels_data['day_of_week'] == 'Sat']


# calculate the average of plays per hour each day
meanplayssun = sunday.groupby('hour posted')['plays'].mean()
meanplaysmon = monday.groupby('hour posted')['plays'].mean()
meanplaystues = tuesday.groupby('hour posted')['plays'].mean()
meanplaysweds = wednesday.groupby('hour posted')['plays'].mean()
meanplaysthurs = thursday.groupby('hour posted')['plays'].mean()
meanplaysfri = friday.groupby('hour posted')['plays'].mean()
meanplayssat = saturday.groupby('hour posted')['plays'].mean()

# convert pandas series to dataframes
sunplays = meanplayssun.to_frame()
monplays = meanplaysmon.to_frame()
tuesplays = meanplaystues.to_frame()
wedsplays = meanplaysweds.to_frame()
thursplays = meanplaysthurs.to_frame()
friplays = meanplaysfri.to_frame()
satplays = meanplayssat.to_frame()


# Set index as new column (hour posted), so that it can be used in the barplot
sunplays.reset_index(inplace=True)
monplays.reset_index(inplace=True)
tuesplays.reset_index(inplace=True)
wedsplays.reset_index(inplace=True)
thursplays.reset_index(inplace=True)
friplays.reset_index(inplace=True)
satplays.reset_index(inplace=True)

# calculate the count of plays per hour each day
postcountsun = sunday.groupby('hour posted')['plays'].count()
postcountmon = monday.groupby('hour posted')['plays'].count()
postcounttues = tuesday.groupby('hour posted')['plays'].count()
postcountweds = wednesday.groupby('hour posted')['plays'].count()
postcountthurs = thursday.groupby('hour posted')['plays'].count()
postcountfri = friday.groupby('hour posted')['plays'].count()
postcountsat = saturday.groupby('hour posted')['plays'].count()

# convert pandas series to dataframes
postcsun = postcountsun.to_frame()
postcmon = postcountmon.to_frame()
postctues = postcounttues.to_frame()
postcweds = postcountweds.to_frame()
postcthurs = postcountthurs.to_frame()
postcfri = postcountfri.to_frame()
postcsat = postcountsat.to_frame()

# Rename the column as 'count'
# Set index as new column (hour posted) in order to be able to add it as a new column to the plays charts
# Set the count column as a variable
# Add count column to each day's plays chart
postcsun.rename({'plays': 'count'}, axis=1, inplace=True)
postcsun.reset_index(inplace=True)
count = postcsun['count']
sunplays['count'] = count

postcmon.rename({'plays': 'count'}, axis=1, inplace=True)
postcmon.reset_index(inplace=True)
count = postcmon['count']
monplays['count'] = count

postctues.rename({'plays': 'count'}, axis=1, inplace=True)
postctues.reset_index(inplace=True)
count = postctues['count']
tuesplays['count'] = count

postcweds.rename({'plays': 'count'}, axis=1, inplace=True)
postcweds.reset_index(inplace=True)
count = postcweds['count']
wedsplays['count'] = count

postcthurs.rename({'plays': 'count'}, axis=1, inplace=True)
postcthurs.reset_index(inplace=True)
count = postcthurs['count']
thursplays['count'] = count

postcfri.rename({'plays': 'count'}, axis=1, inplace=True)
postcfri.reset_index(inplace=True)
count = postcfri['count']
friplays['count'] = count

postcsat.rename({'plays': 'count'}, axis=1, inplace=True)
postcsat.reset_index(inplace=True)
count = postcsat['count']
satplays['count'] = count

# Make bar plots of average plays per hour each day
sunplaysplot = px.bar(sunplays, x="hour posted", y="plays", title="Sunday", hover_data=['count'])
# sunplaysplot.show()

monplaysplot = px.bar(monplays, x="hour posted", y="plays", title="Monday", hover_data=['count'])
# monplaysplot.show()

tuesplaysplot = px.bar(tuesplays, x="hour posted", y="plays", title="Tuesday", hover_data=['count'])
# tuesplaysplot.show()

wedsplaysplot = px.bar(wedsplays, x="hour posted", y="plays", title="Wednesday", hover_data=['count'])
# wedsplaysplot.show()

thursplaysplot = px.bar(thursplays, x="hour posted", y="plays", title="Thursday", hover_data=['count'])
# thursplaysplot.show()

friplaysplot = px.bar(friplays, x="hour posted", y="plays", title="Friday", hover_data=['count'])
# friplaysplot.show()

satplaysplot = px.bar(satplays, x="hour posted", y="plays", title='Saturday', hover_data=['count'])
# satplaysplot.show()

