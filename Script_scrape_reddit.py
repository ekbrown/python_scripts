"""Python script to scrape comments from a subreddit community.
Earl K. Brown, ekbrown byu edu
Note: You'll need to pip install 'praw' and 'pandas' before running this script.
"""

import praw
import pandas as pd
import datetime as dt

# SUPPLY YOUR APP'S INFO
reddit = praw.Reddit(client_id= 'HERE',  # 14-character code
                     client_secret='HERE',  # 27-character code
                     user_agent= 'HERE',  # your app's name
                     username='HERE',  # your reddit username
                     password='HERE')  # your reddit password

# SPECIFY THE SUBREDDIT COMMUNITY YOU WANT TO SCRAPE
subreddit_to_search = 'linguistics'

# SPECIFY THE MAXIMUM NUMBER OF COMMENTS TO SCRAPE
max_comments = 500

# SPECIFY THE PATHWAY TO THE CSV FILE TO SAVE THE TEXT TO
outfile = '/Users/ekb5/Downloads/reddit_comments.csv'

### SAVE THIS SCRIPT AND RUN IT FROM THE COMMAND LINE ###

subreddit = reddit.subreddit(subreddit_to_search)

top_subs = subreddit.top(limit = max_comments)

topics_dict = { "title":[],
                "score":[],
                "id":[], "url":[],
                "comms_num": [],
                "created": [],
                "body":[]}

for i in top_subs:
    topics_dict["title"].append(i.title)
    topics_dict["score"].append(i.score)
    topics_dict["id"].append(i.id)
    topics_dict["url"].append(i.url)
    topics_dict["comms_num"].append(i.num_comments)
    topics_dict["created"].append(i.created)
    topics_dict["body"].append(i.selftext)

topics_data = pd.DataFrame(topics_dict)

def get_date(created):
    return dt.datetime.fromtimestamp(created)

_timestamp = topics_data["created"].apply(get_date)

topics_data = topics_data.assign(timestamp = _timestamp)

topics_data.to_csv(outfile, index=False)

print(f"All done!\nYou should now have a file named {outfile} ready to be imported into spreadsheet software.")
