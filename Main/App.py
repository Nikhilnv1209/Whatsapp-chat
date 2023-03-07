import re
import streamlit as st
import preprocessor
import Helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp chat analyser")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)



#######################################################################################################
    st.markdown("<h1 style='text-align: center; color: rgb(153, 203, 56);'><u>WHATSAPP CHAT ANALYZER</u></h1>",unsafe_allow_html=True)
    ###################################################################################################
    # fetch unique user
    user_list = df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    ###################################################################################################
    #Analysis Starting from here


    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_messages, Link_shared = Helper.fetch_stats(selected_user, df)
        
        st.markdown("<h1 style='text-align: center; color: rgb(153, 203, 56);'><u>TOP STATS</u></h1>",unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages")
            st.subheader(num_messages)

        with col2:
            st.subheader("Total words")
            st.subheader(words)

        with col3:
            st.subheader("Media Shared")
            st.subheader(num_media_messages)

        with col4:
            st.subheader("Link shared")
            st.subheader(Link_shared)




    ###################################################################################################
        #Messages timeline and Daily timeline

        st.markdown("</br><h1 style='text-align: center; color: rgb(153, 203, 56);'><u>TIMELINES</u></h1>",unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h3 style='text-align: center; color: White;'>Message Timeline</h3>",unsafe_allow_html=True)
            monthly_timeline = Helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(monthly_timeline['time'], monthly_timeline['messages'])
            ax.set_xlabel('Month')
            ax.set_ylabel('Messages')
            plt.xticks(rotation='vertical')
            plt.title('Messages Timeline')
            st.pyplot(fig)

        with col2:
            st.markdown("<h3 style='text-align: center; color: White;'>Daily Timeline</h3>",unsafe_allow_html=True)
            daily_timeline = Helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='black')
            ax.set_xlabel('Date')
            ax.set_ylabel('Messages')
            plt.xticks(rotation='vertical')
            plt.title('Daily Timeline')
            st.pyplot(fig)
    



    ###################################################################################################
        # Activity maps

        st.markdown("</br><h1 style='text-align: center; color: rgb(153, 203, 56);'><u>ACTIVITY MAP</u></h1>",unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h3 style='text-align: center; color: white;'>Most Busy Days</h3>",unsafe_allow_html=True)
            most_busy_days = Helper.most_busy_days(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(most_busy_days.index, most_busy_days.values, color='blue')
            ax.set_xlabel('Days')
            ax.set_ylabel('Messages')
            plt.xticks(rotation='vertical')
            plt.title('Most Busy Days')
            st.pyplot(fig)

        with col2:
            st.markdown("<h3 style='text-align: center; color: white;'>Most Busy Months</h3>",unsafe_allow_html=True)
            most_busy_months = Helper.most_busy_months(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(most_busy_months.index, most_busy_months.values, color='orange')
            ax.set_xlabel("Months")
            ax.set_ylabel("Messages")
            plt.xticks(rotation='vertical')
            plt.title('Most Busy Months')
            st.pyplot(fig)




    ###################################################################################################
        # Activity heatmap

        st.markdown("</br><h1 style='text-align: center; color: rgb(153, 203, 56);'><u>WEEKLY ACTIVITY MAP</u></h1>",    unsafe_allow_html=True)
        user_heatmap = Helper.Activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        fig.set_size_inches(10, 6)
        ax = sns.heatmap(user_heatmap)
        ax.set_xlabel("Hours")
        ax.set_ylabel("Days")
        ax.set_title("Message Count by Hour")
        plt.title('Weekly Activity Map')
        st.pyplot(fig)





    ###################################################################################################
        # fetch the most busy users from our dataframe
        if selected_user == 'Overall':
            st.markdown("</br><h1 style='text-align: center; color: rgb(153, 203, 56);'><u>MOST BUSY USERS</u></h1>",unsafe_allow_html=True)
            user_df, perc_df = Helper.fetch_most_busy_user(df)


            col1, col2 = st.columns(2)

            
            with col1:
                st.markdown("<h3 style='text-align: center; color: White;'>By Chart</h3>",unsafe_allow_html=True)
                fig, ax = plt.subplots()
                ax.bar(user_df.user[:10], user_df.counts[:10], color= "red")
                ax.set_xlabel("Users")
                ax.set_ylabel("Messages")
                ax.set_title("Most Busy Users")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.markdown("<h3 style='text-align: center; color: White;'>Percentage Share</h3>",unsafe_allow_html=True)
                st.dataframe(perc_df)




    ###################################################################################################
        #word cloud display
        st.markdown("</br><h1 style='text-align: center; color: rgb(153, 203, 56);'><u>WORD CLOUD</u></h1>",unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        df_wc = Helper.word_cloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.title.set_text('Word Cloud')
        
        st.pyplot(fig)





    ###################################################################################################
        # Most common words
        st.markdown("</br><h1 style='text-align: center; color: rgb(153, 203, 56);'><u>MOST COMMON WORDS</u></h1>",unsafe_allow_html=True)
        most_common_df = Helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.barplot(x=most_common_df['count'], y=most_common_df['words'], orient='h')
        ax.set_xlabel("Words")
        ax.set_ylabel("Count")
        plt.xticks(rotation='vertical')
        plt.title('Most Common Words')
        st.pyplot(fig)

    ###################################################################################################
        
        
        #Sentiment Analysis
        st.markdown("</br><h1 style='text-align: center; color: rgb(153, 203, 56);'><u>SENTIMENT ANALYSIS</u></h1>",unsafe_allow_html=True)




        ##############################################################################################
        

        # Monthly activity map sentiment

        st.markdown("</br><h3 style='text-align: center; color: orange;'>MONTHLY ACTIVITY MAPS(Sentiment)</h3>",unsafe_allow_html=True)
            
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center; color: white;'>Monthly Activity map(Positive)</h3>",unsafe_allow_html=True)
            
            busy_month = Helper.month_activity_map_sentiment(selected_user, df,1)
            busy_month = busy_month.reset_index().rename(columns={'index':'month', 'month':'count'})
            fig, ax = plt.subplots()
            ax = sns.barplot(x='month', y='count', data = busy_month, color = 'green')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
            plt.title('Monthly Activity Map(Positive)')
            st.pyplot(fig)


        with col2:
            st.markdown("<h3 style='text-align: center; color: white;'>Monthly Activity map (Neutral)</h3>",unsafe_allow_html=True)
            
            busy_month = Helper.month_activity_map_sentiment(selected_user, df,0)
            busy_month = busy_month.reset_index().rename(columns={'index':'month', 'month':'count'})
            fig, ax = plt.subplots()
            ax = sns.barplot(x='month', y='count', data = busy_month, color = 'grey')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
            plt.title('Monthly Activity Map(Neutral)')
            st.pyplot(fig)


        with col3:
            st.markdown("<h3 style='text-align: center; color: white;'>Monthly Activity map(Negative)</h3>",unsafe_allow_html=True)
            
            busy_month = Helper.month_activity_map_sentiment(selected_user, df,-1)
            busy_month = busy_month.reset_index().rename(columns={'index':'month', 'month':'count'})
            fig, ax = plt.subplots()
            ax = sns.barplot(x='month', y='count', data = busy_month, color = 'red')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
            plt.title('Monthly Activity Map(Negative)')
            st.pyplot(fig)

        ##############################################################################################

        # Weekly activity map sentiment

        st.markdown("</br><h3 style='text-align: center; color: orange;'>WEEKLY ACTIVITY MAPS(Sentiments)</h3>",unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)


        with col1:
            st.markdown("<h3 style='text-align: center; color: white;'>Weekly Activity Map(Positive)</h3>",unsafe_allow_html=True)
                
            user_heatmap = Helper.weekly_activity_heatmap(selected_user, df, 1)
                
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            ax.set_xlabel("Period")
            ax.set_ylabel("Days")
            plt.title('Weekly Activity Map(Positive)')
            st.pyplot(fig)
            
        with col2:
            
            st.markdown("<h3 style='text-align: center; color: white;'>Weekly Activity Map(Neutra   </h3>",unsafe_allow_html=True)

            user_heatmap = Helper.weekly_activity_heatmap(selected_user, df, 0)

            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            ax.set_xlabel("Period")
            ax.set_ylabel("Days")
            plt.title('Weekly Activity Map(Neutral)')
            st.pyplot(fig)
            
        with col3:
            
            st.markdown("<h3 style='text-align: center; color: white;'>Weekly Activity Map(Negative</h3>",unsafe_allow_html=True)
            
            user_heatmap = Helper.weekly_activity_heatmap(selected_user, df, -1)
            
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            ax.set_xlabel("Period")
            ax.set_ylabel("Days")
            plt.title('Weekly Activity Map(Negative)')
            st.pyplot(fig)
            
        
        #############################################################################################


        # Daily activity map sentiment

        st.markdown("</br><h3 style='text-align: center; color: orange;'>DAILY ACTIVITY MAPS(Sentiments)</h3>",unsafe_allow_html=True)


        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center; color: white;'>Daily Activity map(Positive)</h3>",unsafe_allow_html=True)
            
            busy_day = Helper.daily_activity_map_sentiment(selected_user, df,1)
            busy_day = busy_day.reset_index().rename(columns={'index':'day', 'day_name':'count'})
            fig, ax = plt.subplots()
            ax = sns.barplot(x='day', y='count', data = busy_day, color = 'green')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
            plt.title('daily Activity Map(positive)')
            st.pyplot(fig)

        with col2:
            st.markdown("<h3 style='text-align: center; color: white;'>Daily Activity map(Neutral)</h3>",unsafe_allow_html=True)
            
            busy_day = Helper.daily_activity_map_sentiment(selected_user, df,0)
            busy_day = busy_day.reset_index().rename(columns={'index':'day', 'day_name':'count'})
            fig, ax = plt.subplots()
            ax = sns.barplot(x='day', y='count', data = busy_day, color = 'grey')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
            plt.title('daily Activity Map(Neutral)')
            st.pyplot(fig)

        with col3:
            st.markdown("<h3 style='text-align: center; color: white;'>Daily Activity map(Negative)</h3>",unsafe_allow_html=True)
            
            busy_day = Helper.daily_activity_map_sentiment(selected_user, df,-1)
            busy_day = busy_day.reset_index().rename(columns={'index':'day', 'day_name':'count'})
            fig, ax = plt.subplots()
            ax = sns.barplot(x='day', y='count', data = busy_day, color = 'red')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
            plt.title('daily Activity Map(Negative)')
            st.pyplot(fig)



        #############################################################################################
       

        # Daily timeline sentiment

        st.markdown("</br><h3 style='text-align: center; color: orange;'>DAILY TIMELINE(SENTIMENTAL)</h3>",unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center; color: white;'>Daily Timeline(Positive)</h3>",unsafe_allow_html=True)
            
            daily_timeline = Helper.daily_timeline_sentiment(selected_user, df, 1)
            
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='green')
            ax.set_xlabel("Date")
            ax.set_ylabel("Messages")
            ax.set_title('Daily Timeline(Positive)')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        with col2:
            st.markdown("<h3 style='text-align: center; color: white;'>Daily Timeline(Neutral)</h3>",unsafe_allow_html=True)
            
            daily_timeline = Helper.daily_timeline_sentiment(selected_user, df, 0)
            
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='grey')
            ax.set_xlabel("Date")
            ax.set_ylabel("Messages")
            ax.set_title('Daily Timeline(Neutral)')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        with col3:
            st.markdown("<h3 style='text-align: center; color: white;'>Daily Timeline(Negative)</h3>",unsafe_allow_html=True)
            
            daily_timeline = Helper.daily_timeline_sentiment(selected_user, df, -1)
            
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='red')
            ax.set_xlabel("Date")
            ax.set_ylabel("Messages")
            ax.set_title('Daily Timeline(Negative)')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        ###############################################################################################

        # USERS CONTRIBUTION BASED ON SENTIMETS


        # Percentage contributed
        if selected_user == 'Overall':
            st.markdown("</br><h3 style='text-align: center; color: orange;'>USERS CONTRIBUTION BASED ON SENTIMENTS</h3>",unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
            with col1:
                st.markdown("<h3 style='text-align: center; color: white;'>Most Positive Contribution</h3>",unsafe_allow_html=True)
                x = Helper.percentage_sentiment(df, 1)
                
                # Displaying
                st.dataframe(x, width=300, height=320)
            with col2:
                st.markdown("<h3 style='text-align: center; color: white;'>Most Neutral Contribution</h3>",unsafe_allow_html=True)
                y = Helper.percentage_sentiment(df, 0)
                
                # Displaying
                st.dataframe(y, width=300, height=320)
            with col3:
                st.markdown("<h3 style='text-align: center; color: white;'>Most Negative Contribution</h3>",unsafe_allow_html=True)
                z = Helper.percentage_sentiment(df, -1)
                
                # Displaying
                st.dataframe(z, width=300, height=320)
            
        ###############################################################################################
        
        # Most Positive,Negative,Neutral User...

        if selected_user == 'Overall':
            st.markdown("</br><h3 style='text-align: center; color: orange;'>MOST USERS PER SENTIMENT</h3>",unsafe_allow_html=True)

            # Getting names per sentiment
            x = df['users'][df['value'] == 1].value_counts().head(10)
            y = df['users'][df['value'] == -1].value_counts().head(10)
            z = df['users'][df['value'] == 0].value_counts().head(10)

            col1,col2,col3 = st.columns(3)

            with col1:
                # heading
                st.markdown("<h3 style='text-align: center; color: white;'>Most Positive Users</h3>",unsafe_allow_html=True)
                
                # Displaying
                fig, ax = plt.subplots()
                ax = sns.barplot(x=x.index, y=x.values, color='green',orient='v')
                ax.set_xlabel("Messages")
                ax.set_ylabel("Users")
                ax.set_title("Top 10 Users With Positive Messages")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                # heading
                st.markdown("<h3 style='text-align: center; color: white;'>Most Neutral Users </h3>",unsafe_allow_html=True)
                
                # Displaying
                fig, ax = plt.subplots()
                ax = sns.barplot(x=z.index, y=z.values, color='grey',orient='v')
                ax.set_xlabel("Messages")   
                ax.set_ylabel("Users")
                ax.set_title("Top 10 Users With Neutral Messages")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col3:
                # heading
                st.markdown("<h3 style='text-align: center; color: white;'>Most Negative Users</h3>",unsafe_allow_html=True)
                
                # Displaying
                fig, ax = plt.subplots()
                ax = sns.barplot(x=y.index, y=y.values, color='red',orient='v')
                ax.set_xlabel("Messages")
                ax.set_ylabel("Users")
                ax.set_title("Top 10 Users With Negative Messages")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)


        ###############################################################################################

        # Word cloud of Positive , negative and neutral words

        st.markdown("</br><h3 style='text-align: center; color: orange;'>WORD CLOUDS(Sentiment)</h3>",unsafe_allow_html=True)

        col1,col2,col3 = st.columns(3)
        
        with col1:
           
                st.markdown("<h3 style='text-align: center; color: white;'>Positive WordCloud</h3>",unsafe_allow_html=True)
                
                # Creating wordcloud of positive words
                df_wc = Helper.create_wordcloud_sentiment(selected_user, df,1)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                fig.set_size_inches(5,5)
                ax.set_title('Positive WordCloud')
                st.pyplot(fig)
           
            
        with col2:
         
                st.markdown("<h3 style='text-align: center; color: white;'>Neutral WordCloud</h3>",unsafe_allow_html=True)
                
                # Creating wordcloud of neutral words
                df_wc = Helper.create_wordcloud_sentiment(selected_user, df,0)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                ax.set_title('Neutral WordCloud')
                st.pyplot(fig)
          
        with col3:
                # heading
                st.markdown("<h3 style='text-align: center; color: white;'>Negative WordCloud</h3>",unsafe_allow_html=True)
                
                # Creating wordcloud of negative words
                df_wc = Helper.create_wordcloud_sentiment(selected_user, df,-1)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                ax.set_title('Negative WordCloud')
                st.pyplot(fig)
        



    ###################################################################################################
        # Most emojies shared
        st.markdown("</br><h1 style='text-align: center; color: rgb(153, 203, 56);'><u>EMOJI ANALYSIS</u></h1>",unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        emoji_df = Helper.emoji_count(selected_user, df)

        with col1:
            st.markdown("<h3 style='text-align: center; color: White;'>Pie chart Share</h3>",unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct='%0.2f')
            ax.axis('equal')
            st.pyplot(fig) 
            
        
        with col2:
            st.markdown("<h3 style='text-align: center; color: White;'>Emoji Shared</h3>",unsafe_allow_html=True)
            st.dataframe(emoji_df,width=600, height=250)
        

