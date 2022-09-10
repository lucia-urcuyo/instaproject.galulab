import json
import requests
import pandas as pd
import matplotlib.pyplot as plt


# Function 1: Asks for a URL and returns media IDs into a dataframe
def link_to_mediaID(link):
    try:
        dm = requests.get(link)
        mid = json.loads(dm.content)
        jid = (mid.get('data'))
        dfID = pd.DataFrame.from_dict(jid)
        return dfID
    except:
        print("An error occurred. Invalid URL")


# Function 2: Asks for media ID and desired attribute and returns the data
def data_from_mediaID(mediaID, attribute_type):
    domain2 = 'https://graph.facebook.com/v3.0/'

    try:
        aurl = domain2 + mediaID + '/insights/' + attribute_type + '?' + access_token
        dmid = requests.get(aurl)
        dd = json.loads(dmid.content)
        z = dd['data'][0]
        attribute_d = z.get('values')
        ad = pd.DataFrame.from_dict(attribute_d)
        return ad.iloc[0, 0]
    except:
        # Attribute must be one of the following values: impressions, reach, carousel_album_impressions,
        # carousel_album_reach, carousel_album_engagement, carousel_album_saved, carousel_album_video_views,
        # taps_forward, taps_back, exits, replies, engagement, saved, video_views, likes, comments, shares,
        # plays, total_interactions, follows, profile_visits, profile_activity, navigation"
        return (0)


# Function 3: Asks for media ID and desired fields and returns the data
def data_from_mediaID2(mediaID, field):
    domain3 = 'https://graph.facebook.com/v14.0/'

    try:
        furl = domain3 + mediaID + '?fields=' + field + '&' + access_token
        mediafd = requests.get(furl)
        fdata = json.loads(mediafd.content)
        fd = fdata.get(field)

        return fd
    except:
        return (0)


# First part of our URL
domain = "https://graph.facebook.com/v9.0/"

# Always stays the same, no need to change, 2nd part of URL
my_insta_id = "17841446768661835"

# Need to generate a new one every 60 min, 4th part of URL
access_token = "access_token=EAAP6OFrPKd8BAPZAJ8XeDxZCobpVdtS1iTZAu3UruACDfGGE3DYl804Xx5z1Pn3CZC6D3yJGMSWPCNMZCw6qznfzT61O9kyUIWNQge2EBzE4hqDswT4yZB7vTpAHNyNlE385bfWCbuZCF2dpDYoIrpOy3ZBchevHXrsjk1CcPdn6VsgvDaDoiv7rxHZBiNyIzkb8Uqp78bLq8LI6M1Lqg5bFz2ah5ZA0RjupW5MiuC3HUaizZC6DbCOKzU3YYpZBwTZCp2lkZD"

# Build URL
urlformedia = domain + my_insta_id + "/media?" + access_token

# Pull data from URL
datamedia = requests.get(urlformedia)
mediaID = json.loads(datamedia.content)

counter = 1

urllist = [0, 0, 0, 0]

urllist[0] = urlformedia

while counter < 4:
    # Grab URL and make it a json object

    x = requests.get(urllist[counter - 1])
    y = json.loads(x.content)

    # Get the next URL from the json object

    a = y.get('paging')
    b = a.get('next')

    # Store next URL in the next position

    urllist[counter] = b

    # Add one to our counter to keep track of loops

    counter += 1

# Save media ID data frame from each URL page
p1 = link_to_mediaID(urllist[0])
p2 = link_to_mediaID(urllist[1])
p3 = link_to_mediaID(urllist[2])
p4 = link_to_mediaID(urllist[3])

# Joins media ID 1, 2, 3, 4
IDlist = pd.concat([p1, p2, p3, p4])

# Forloop to get attribute values for each media id

plays = []
likes = []
comments = []
impressions = []
engagement = []
reach = []
saved = []
shares = []
total_interactions = []
follows = []
profile_visits = []
profile_activity = []
navigation = []
timestamp = []
permalink = []
caption = []

for i in IDlist['id']:
    plays.append(data_from_mediaID(i, 'plays'))
    likes.append(data_from_mediaID(i, 'likes'))
    comments.append(data_from_mediaID(i, 'comments'))
    impressions.append(data_from_mediaID(i, 'impressions'))
    engagement.append(data_from_mediaID(i, 'engagement'))
    reach.append(data_from_mediaID(i, 'reach'))
    saved.append(data_from_mediaID(i, 'saved'))
    shares.append(data_from_mediaID(i, 'shares'))
    total_interactions.append(data_from_mediaID(i, 'total_interactions'))
    follows.append(data_from_mediaID(i, 'follows'))
    profile_visits.append(data_from_mediaID(i, 'profile_visits'))
    profile_activity.append(data_from_mediaID(i, 'profile_activity'))
    navigation.append(data_from_mediaID(i, 'navigation'))
    timestamp.append(data_from_mediaID2(i, 'timestamp'))
    permalink.append(data_from_mediaID2(i, 'permalink'))
    caption.append(data_from_mediaID2(i, 'caption'))

# Add timestampt to ID list
IDlist['timestamp'] = timestamp

# Split timestamp into 2 columns: date and time
timestamp = IDlist['timestamp'].str.split(pat='T', n=-1, expand=True)
date = IDlist['date'] = timestamp[0]
time = IDlist['time'] = timestamp[1]

# Create 2 columns with the name of the week day and the number of the week day
IDlist['my dates'] = pd.to_datetime(IDlist['date'])
IDlist['num_day_of_week'] = IDlist['my dates'].dt.dayofweek

days = {0: 'Mon', 1: 'Tues', 2: 'Weds', 3: 'Thurs', 4: 'Fri', 5: 'Sat', 6: 'Sun'}

IDlist['day_of_week'] = IDlist['num_day_of_week'].apply(lambda x: days[x])

num_day_of_week = IDlist['num_day_of_week']
day_of_week = IDlist['day_of_week']

# Add attribute values columns to ID list dataframe
IDlist['plays'] = plays
IDlist['likes'] = likes
IDlist['comments'] = comments
IDlist['impressions'] = impressions
IDlist['engagement'] = engagement
IDlist['reach'] = reach
IDlist['saved'] = saved
IDlist['shares'] = shares
IDlist['total_interactions'] = total_interactions
IDlist['follows'] = follows
IDlist['profile_visits'] = profile_visits
IDlist['profile_activity'] = profile_activity
IDlist['navigation'] = navigation
IDlist['date'] = date
IDlist['time'] = time
IDlist['num_day_of_week'] = num_day_of_week
IDlist['day_of_week'] = day_of_week
IDlist['permalink'] = permalink
IDlist['caption'] = caption

# Forloop to count number of hastags for each post
cap = IDlist['caption'].iloc[0]

hashtags = []

for cap in IDlist['caption']:

        hashtag_count = 0

        for hasht in cap:

                if hasht == '#':
                        hashtag_count = hashtag_count + 1

        hashtags.append(hashtag_count)

# Add hashtags column to IDlist dataframe
IDlist['hashtags'] = hashtags

# Split time into 3 columns: hour, minutes, seconds
time2 = IDlist['time'].str.split(pat=':', n=-1, expand=True)

# Add hour posted column to IDlist
IDlist['hour posted'] = time2[0]

# Reverse order and reindex dataframe
IDlist = IDlist.iloc[::-1]
IDlist = IDlist.reset_index(drop=True)

# Select rows where plays = 0
PhotosData = IDlist[IDlist['plays'] == 0]
IDPD = PhotosData
IDPD = IDPD.index.tolist()

# Create new data frame with the removed rows selected above
ReelsData = IDlist.drop(
        labels=IDPD,
        axis=0,
        inplace=False)

# Drop all columns that dont apply to reels and columns that we don't need (timestamp, my dates and time)
ReelsData = ReelsData.drop(
        labels=["impressions", "engagement", "follows", "profile_visits", "profile_activity", "navigation", "timestamp",
                'time', 'my dates'],
        axis=1,
        inplace=False)

print(ReelsData)

print(PhotosData)