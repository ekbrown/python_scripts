"""Python function to extract comments below videos on Youtube,
and return a Pandas DataFrame.
Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)
Note: You must pip install Python modules 'youtube', 'requests', and 'pandas' before running this script.   
"""

def scrape_yt_comments(api_key, client_id, client_secret, lst_of_ids, num_comments = 50):
    """Access Youtube's API with user's app credentials to scrape comments from videos.
    param api_key: the user's (your) Youtube API key as a string.
    param client_id: the user's Youtube app client ID as a string.
    param client_secret: the user's Youtube app client secret as a string.
    param lst_of_ids: a Python list of video IDs as strings.
    param num_comments: the maximum number of comments to collect per video, as an integer.
    return value: a Pandas DataFrame.
    """

    import json, pandas as pd, requests
    from youtube import API

    api = API(client_id=client_id, client_secret=client_secret, api_key=api_key)

    df = pd.DataFrame(columns = ['video_id' , 'video_name', 'comment_author' , 'comment_timestamp', "comment_text"])

    for id in lst_of_ids:

        print(f"working on {id}")
        video = api.get('videos', id=id)

        # get title of current video
        cur_title = video['items'][0]['snippet']['title']

        # retrieve comments as JSON-formatted string
        url = f"https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&textFormat=plainText&part=snippet&videoId={id}&maxResults={num_comments}"
        comments = requests.get(url)

        # convert JSON-formatted string to Python dictionary
        comments_dict = json.loads(comments.text)

        # loop over comments, saving to collector DataFrame
        for c in comments_dict['items']:
            author = c['snippet']['topLevelComment']['snippet']['authorDisplayName']
            txt = c['snippet']['topLevelComment']['snippet']['textDisplay']
            timestamp = c['snippet']['topLevelComment']['snippet']['updatedAt']

            df = df.append({'video_id' : id , 'video_name' : cur_title, "comment_author": author, "comment_timestamp":timestamp, "comment_text":txt} , ignore_index=True)

    return df

### test the function
api_key = "YOUR_KEY_HERE"
client_id = "YOUR_CLIENTE_ID_HERE"
client_secret = "YOUR_CLIENT_SECRET_HERE"
ids = ["bjuzxHcVrNs", "RQABjI0tArw"]
results = scrape_yt_comments(api_key, client_id, client_secret, ids)

# save Pandas DataFrame to hard drive as CSV file; ***update pathway***
results.to_csv("path/to/directory/youtube_comments.csv", sep = "\t", index = False)
