"""Python script to extract the closed captions generated by
automated speech recognition on Youtube vidoes, and return a Pandas DataFrame.
Uses the easy-to-use YouTubeTranscriptApi module created by Jonas Depoix.
Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)
(c) 2020
"""

# def get_ytcc(video_id, lang = "en"):
def get_ytcc(video_id):
    """Get closed caption transcript of Youtube video created by ASR.
    param video_id: Youtube video ID, visible in the URL after "v=".
    param lang: language of speech in video; defaults to "en".
    return value: Pandas DataFrame with three columns: text, start, duration.
    """
    from youtube_transcript_api import YouTubeTranscriptApi
    import pandas as pd
    txt = YouTubeTranscriptApi.get_transcript(video_id)
    return pd.DataFrame(txt)

### test the function
print(get_ytcc("dj9RR4BSqvM"))  # "Keynote: Katie Bell - How Python works as a teaching language"
