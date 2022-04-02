from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    # 1. fetch no. of messages
    num_messages = df.shape[0]
    # 2. number of words
    words = 0
    links = 0
    for w in df['Message']:
        words += len(w.split())
        links += len(extract.find_urls(w))

    # 3.
    num_of_media = df[df['Message'] == ' <Media omitted>\n'].shape[0]

    return num_messages, words, num_of_media, links

# ======================================================================================================================


def most_busy_users(df):
    df = df[df['User'] != 'Group_notification']
    x = df['User'].value_counts().head()
    d = round((df["User"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index':'name', 'User':'percent'})
    return x, d

# ======================================================================================================================


def create_wordcloud(selected_user, df):
    f = open("./stop_hinglish.txt", 'r')
    stop_word = f.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'Group_notification']
    temp = temp[temp['Message'] != " <Media omitted>\n"]

    def remove_stop_words(mess):
        y = []
        for word in mess.lower().split():
            if word not in stop_word:
                y.append(word)

        if len(y) == 0:
            return ''
        return ' '.join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='black')
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    temp = temp[temp['Message'] != ""]
    if temp['Message'].shape[0] > 0:
        df_wc = wc.generate(temp['Message'].str.cat(sep=' '))
        return df_wc

# ======================================================================================================================


def most_common_words(selected_user, df):
    f = open("./stop_hinglish.txt", 'r')
    stop_word = f.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    temp = df[df['User'] != 'Group_notification']
    temp = temp[temp['Message'] != " <Media omitted>\n"]

    words = []
    for mess in temp['Message']:
        for word in mess.lower().split():
            if word not in stop_word:
                words.append(word)

    if len(words) == 0:
        return None

    most_common_word = pd.DataFrame(Counter(words).most_common(20)).rename(columns={0: 'Words', 1: 'Count'})
    return most_common_word

# ======================================================================================================================


def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emo = []
    for mess in df["Message"]:
        emo.extend([c for c in mess if c in emoji.UNICODE_EMOJI['en']])

    if len(emo) == 0:
        return pd.DataFrame()

    return pd.DataFrame(Counter(emo).most_common(len(Counter(emo)))).rename(columns={0: 'Emojis', 1: 'Count'})

# ======================================================================================================================


def Time_line_df(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'Month_num', 'Month']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i]+'-'+str(timeline['Year'][i]))

    timeline['Time'] = time
    return timeline

# ======================================================================================================================


def daily_Time_line_df(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    timeline_ = df.groupby(['date']).count()['Message'].reset_index()

    return timeline_

# ======================================================================================================================


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['day_name'].value_counts()

# ======================================================================================================================


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Month'].value_counts()


# ======================================================================================================================


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)

# ======================================================================================================================
