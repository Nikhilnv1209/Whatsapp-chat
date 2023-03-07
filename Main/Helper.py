from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
from textblob import TextBlob
import emoji
extract = URLExtract()


#######################################################################################################
# 1. fetch the number of messages
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # 1.fetch the number of messages
    num_messages = df.shape[0]

    # 2.fetch the total number of words
    words = []
    for message in df['messages']:
        if(message != '<Media omitted>\n'):
            words.extend(message.split())

    # 3. fetch number of media messages
    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

    # 4. fetch number of links shared
    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


########################################################################################################
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
        
    monthly_timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time = []
    for i in range(monthly_timeline.shape[0]):
        time.append(monthly_timeline['month'][i] + '-' + str(monthly_timeline['year'][i]))
    monthly_timeline['time'] = time
    
    return monthly_timeline




def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

#####################################################################################################


def most_busy_days(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    daily_activity = df['day_name'].value_counts()
    return daily_activity


#####################################################################################################

def most_busy_months(selected_user,df):
        
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
        
    monthly_activity = df['month'].value_counts()
    return monthly_activity


#####################################################################################################


def Activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap

#####################################################################################################


def fetch_most_busy_user(df):
    df = df[df['users'] != 'Group notification']
    users_df = df['users'].value_counts().reset_index()
    users_df.rename(columns = {'index': 'user', 'users': 'counts'}, inplace = True)
    prec_df = round(df['users'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'index':'user', 'users':'percent'})
    return users_df, prec_df


########################################################################################################

def word_util(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # removing group notification messages
    df_user_chat = df[df['users'] != 'Group notification']
    # removing media messages
    df_user_chat = df_user_chat[df_user_chat['messages'] != '<Media omitted>\n']

    f = open('./Hinglish_words.txt','r',encoding='utf-8')
    stop_words = f.read().lower().split('\n')

    words = []
    for message in df_user_chat['messages']:
        for word in message.split():
            if word not in stop_words:
                words.append(word)
    
    return words




def word_cloud(selected_user, df):
    
    words = word_util(selected_user, df)
    wc = WordCloud(width=500, height=500, min_font_size=7, background_color='white')
    df_wc = wc.generate(' '.join(words))
    return df_wc
    
########################################################################################################

def most_common_words(selected_user , df):
    
    words = word_util(selected_user, df)
    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['words', 'count'])
    return most_common_df

########################################################################################################



def month_activity_map_sentiment(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    df = df[df['value'] == k]
    return df['month'].value_counts()

####################################################################################################

def weekly_activity_heatmap(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df = df[df['value'] == k]
    
    # Creating heat map
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap

####################################################################################################

def daily_activity_map_sentiment(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    df = df[df['value'] == k]
    return df['day_name'].value_counts()

######################################################################################################

def daily_timeline_sentiment(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df = df[df['value']==k]
    # count of message on a specific date
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline


######################################################################################################

# Will return percentage of message contributed having k(0/1/-1) sentiment
def percentage_sentiment(df,k):
    df = round((df['users'][df['value']==k].value_counts() / df[df['value']==k].shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return df

######################################################################################################


# Return wordcloud from words in message

def word_util_sentiment(selected_user, df,k):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # removing group notification messages
    df_user_chat = df[df['users'] != 'Group notification']
    # removing media messages
    df_user_chat = df_user_chat[df_user_chat['messages'] != '<Media omitted>\n']

    f = open('./Hinglish_words.txt','r',encoding='utf-8')
    stop_words = f.read().lower().split('\n')

    words = []
    for message in df_user_chat['messages']:
        for word in message.split():
            if word not in stop_words:
                words.append(word)

    if k == 1:
        words = [word for word in words if TextBlob(word).sentiment.polarity > 0]
    elif k == -1:
        words = [word for word in words if TextBlob(word).sentiment.polarity < 0]
    else:
        words = [word for word in words if TextBlob(word).sentiment.polarity == 0]
    
    return words




def create_wordcloud_sentiment(selected_user,df,k):
    words = word_util_sentiment(selected_user, df, k)
    wc = WordCloud(width=800, height=800, min_font_size=7, background_color='white')
    df_wc = wc.generate(' '.join(words))
    return df_wc
    
    

########################################################################################################
def emoji_count(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    
    emojis = []
    for message in df['messages']:
        for c in message:
            if c in emoji.EMOJI_DATA:
                emojis.extend(c)
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(20), columns=['emoji', 'count'])
    return emoji_df



########################################################################################################



































