import re
import pandas as pd



def preprocess(data):
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w\w\s-"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_dates': dates})

    # convert message_date type
    df['message_dates'] = pd.to_datetime(df['message_dates'], format='%m/%d/%y, %H:%M %p -')

    df.rename(columns={'message_dates': 'date'}, inplace=True)

    # seperate name and message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split("([\w\W]+?):\s", message)
        if (entry[1:]):  # username
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group notification')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period




    ############################################################################################
    # # VADER : is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments.
    import nltk
    # import ssl

    # try:
    #     _create_unverified_https_context = ssl._create_unverified_context
    # except AttributeError:
    #     pass
    # else:
    #     ssl._create_default_https_context = _create_unverified_https_context


    # nltk.download('vader_lexicon')
    
        #sentiment requirements
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

        # Object
    sentiments = SentimentIntensityAnalyzer()

    # Creating different columns for (Positive/Negative/Neutral)
    df["po"] = [sentiments.polarity_scores(i)["pos"] for i in df["messages"]] # Positive
    df["ne"] = [sentiments.polarity_scores(i)["neg"] for i in df["messages"]] # Negative
    df["nu"] = [sentiments.polarity_scores(i)["neu"] for i in df["messages"]] # Neutral

    # To indentify true sentiment per row in message column
    def sentiment(d):
        if d["po"] >= d["ne"] and d["po"] >= d["nu"]:
            return 1
        if d["ne"] >= d["po"] and d["ne"] >= d["nu"]:
            return -1
        if d["nu"] >= d["po"] and d["nu"] >= d["ne"]:
            return 0
    # Creating new column & Applying function
    df['value'] = df.apply(lambda row: sentiment(row), axis=1)

    return df