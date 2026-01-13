import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
import regex as re

extract = URLExtract()

# 1 ===========================================================
def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for msg in df['message']:
        words.extend(str(msg).split())

    media_count = df[df['message']=="<Media omitted>"].shape[0]

    links = []
    for msg in df['message']:
        links.extend(extract.find_urls(str(msg)))

    return num_messages, len(words), media_count, len(links)


# 2 ===========================================================
def monthly_timeline(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user']==selected_user]

    timeline = df.groupby(['year','month_num','month'])['message'].count().reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline


# 3 ===========================================================
def daily_timeline(selected_user,df):

    if selected_user!="Overall":
        df = df[df['user']==selected_user]

    daily = df.groupby('only_date')['message'].count().reset_index()
    return daily


# 4 ===========================================================
def week_activity_map(selected_user,df):

    if selected_user!="Overall":
        df = df[df['user']==selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):

    if selected_user!="Overall":
        df = df[df['user']==selected_user]

    return df['month'].value_counts()


# 5 ===========================================================
def most_busy_users(df):

    x = df['user'].value_counts().head()
    percent = (df['user'].value_counts()/df.shape[0]*100).reset_index()
    percent.columns=['name','percent']
    return x, percent


# 6 ===========================================================
def create_wordcloud(selected_user,df):

    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    wc = WordCloud(width=500,height=300,background_color="white")
    img = wc.generate(" ".join(df['message']))
    return img


# 7 ===========================================================
def most_common_words(selected_user,df):

    stop_words = open("extracted_stopwords.txt","r",encoding="utf-8").read()

    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    temp = df[df['message']!="<Media omitted>"]

    words=[]
    for msg in temp['message']:
        for w in str(msg).lower().split():
            if w not in stop_words:
                words.append(w)

    df_out = pd.DataFrame(Counter(words).most_common(20),columns=['word','count'])
    return df_out


# 8 ===========================================================
def emoji_helper(selected_user,df):

    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    chars=[]
    for msg in df['message']:
        chars.extend(re.findall(r'\X',msg))

    emojis=[c for c in chars if c in emoji.EMOJI_DATA]

    return pd.DataFrame(Counter(emojis).most_common(),columns=['emoji','count'])


# 9 🔥 HEATMAP FUNCTION =======================================
def activity_heatmap(selected_user,df):

    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return heatmap
