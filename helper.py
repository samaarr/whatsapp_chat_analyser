import matplotlib.pyplot as plt
from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
import re
import sys

extractor = URLExtract()

def fetch_stats(selected_user, df):
#
#     if selected_user != 'Overall':
#         df = df[df['user']== selected_user]
#
#         #fetch no of messages
#         num_messages = df.shape[0]

        # #fetch no of words
        # words = []
        # for messages in df['message']:
        #     words.extend(messages.split())
        #
        # #fetch no of media shared
        # num_media_messages = df[df['message'] == '<Media omitted>/n'].shape[0]
        #
        # #fetch no of links shared
        # links = []
        # for message in df['message']:
        #     links.extend(extractor.find_urls(message))
        #
        # return num_messages, len(words), len(num_media_messages), len(links)



    if selected_user == 'Overall':

        num_messages = df.shape[0]

        words = []
        for messages in df['message']:
            words.extend(messages.split())

        #fetch no of media shared
        num_media_messages = []
        for media in df['message']:
            if media == '<Media omitted>\n':
                num_media_messages.append(media)



        #fetch no of links shared
        links = []
        for message in df['message']:
            links.extend(extractor.find_urls(message))

        return num_messages, words, num_media_messages, links



    else:
        new_df = df[df['user']== selected_user]
        num_messages = new_df.shape[0]
        words = []
        for messages in new_df['message']:
            words.extend(messages.split())

        # fetch no of media shared
        # num_media_messages = new_df[df['message'] == '<Media omitted>\n'].shape[0]
        num_media_messages = []
        for media in new_df['message']:
            if media == '<Media omitted>\n':
                num_media_messages.append(media)

        # fetch no of links shared
        links = []
        for message in new_df['message']:
            links.extend(extractor.find_urls(message))

        return num_messages, words, num_media_messages, links

def most_busy_users(df):
    x = df['user'].value_counts()
    percent_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, percent_df

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    f= open('stopwords_hinglish.txt')
    stopwords = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['noemoji_message']:
        for word in message.split():
                if word.lower() not in stopwords:
                    words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

def most_common_emojis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    most_common_emoji = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return most_common_emoji

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def weekly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    activity_heat = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return activity_heat

