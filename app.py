import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Analyser- Samar Patil https://github.com/samaarr')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

     bytes_data = uploaded_file.getvalue()
     data = bytes_data.decode('utf-8')
     df= preprocessor.preprocess(data)


     #fetch unique users
     user_list = df['user'].unique().tolist()
     user_list.remove('group_notification')
     user_list.sort()
     user_list.insert(0, 'Overall')

     selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

     if st.sidebar.button("Show Analysis"):
          num_messages, words, media, links = helper.fetch_stats(selected_user, df)

          st.title('Top Stats')
          col1, col2, col3, col4 = st.columns(4)

          with col1:
               st.header('Total messages')
               st.title(num_messages)
          with col2:
               st.header('Total words')
               st.title(len(words))
          with col3:
               st.header('Total media')
               st.title(len(media))
          with col4:
               st.header('Total links')
               st.title(len(links))

          #monthly timeline
          st.title('Monthly Timeline')
          timeline = helper.monthly_timeline(selected_user,df)
          fig, ax = plt.subplots()
          ax.plot(timeline['time'], timeline['message'])
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          #daily timeline
          st.title('Daily Timeline')
          daily_timeline = helper.daily_timeline(selected_user, df)
          fig, ax = plt.subplots()
          ax.plot(daily_timeline['only_date'], daily_timeline['message'])
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          #activity map
          st.title('Activity Map')
          col1,col2 = st.beta_columns(2)

          with col1:
               st.header("most busy day")
               busy_day = helper.weekly_activity(selected_user,df)
               fig,ax = plt.subplots()
               ax.bar(busy_day.index, busy_day.values, color='red')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)
          with col2:
               st.header("most busy month")
               busy_month = helper.monthly_activity(selected_user, df)
               fig, ax = plt.subplots()
               ax.bar(busy_month.index, busy_month.values, color='green')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)

          st.title('Weekly Activity map')
          activity_heat = helper.activity_heatmap(selected_user,df)
          fig, ax =plt.subplots()
          ax= sns.heatmap(activity_heat)
          st.pyplot(fig)



          #finding busiest user
          if selected_user == 'Overall':
               x, percent_df = helper.most_busy_users(df)
               st.title('Most Busy Users')

               fig, ax = plt.subplots()
               col1, col2 = st.columns(2)

               with col1:
                    ax.bar(x.index, x.values)
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
               with col2:
                    st.dataframe(percent_df)

          #most_common_words
          st.title('Most used Words')
          most_common_msg = helper.most_common_words(selected_user, df)
          st.dataframe(most_common_msg)

          # emoji analysis
          st.title('Most used Emojis')
          emoji_df = helper.most_common_emojis(selected_user,df)

          col1, col2 = st.beta_columns(2)

          with col1:
               st.dataframe(emoji_df)
               with col2:
                    fig, ax = plt.subplots()
                    ax.pie (emoji_df[1], labels= emoji_df[0])
                    st.pyplot(fig)

