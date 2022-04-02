import streamlit as st
import preposessor, Helper
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

st.sidebar.title("Whatsapp chat analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preposessor.preprocess(data)

    st.markdown("<h1 style='text-align: center; color: red;'>Top Statistics</h1>", unsafe_allow_html=True)

    user_list = df['User'].unique().tolist()
    if 'Group_notification' in user_list:
        user_list.remove('Group_notification')
    user_list.sort()
    user_list = ["Overall"] + user_list

    selected_user = st.sidebar.selectbox("Show analysis wrt",  user_list)

    if st.sidebar.button("Show Analysis"):

        st.markdown("<h2 style='text-align: left; color: yellow;'>All Messages</h2>", unsafe_allow_html=True)
        if selected_user != 'Overall':
            df = df[df['User'] == selected_user]
        st.dataframe(df)

        num_messages, words, media, links = Helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header('Media Shared')
            st.title(media)

        with col4:
            st.header('Total   Links')
            st.title(links)

# ======================================================================================================================

        # Timeline
        st.markdown("<h2 style='text-align: left; color: yellow;'>Monthly Timeline</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        timeline = Helper.Time_line_df(selected_user, df)
        with col1:
            fig, ax = plt.subplots()
            ax.plot(timeline['Time'], timeline['Message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(timeline)

# # ======================================================================================================================
#
        # daily Timeline
        st.markdown("<h2 style='text-align: left; color: yellow;'>Daily Timeline</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        timeline_ = Helper.daily_Time_line_df(selected_user, df)
        # st.dataframe(timeline_)
        with col1:
            st.dataframe(timeline_)
        with col2:
            fig, ax = plt.subplots()
            ax.plot(timeline_['date'], timeline_['Message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
#
# # ======================================================================================================================
#
        # activity map
        st.markdown("<h2 style='text-align: left; color: yellow;'>Most busy day</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        busy_day = Helper.week_activity_map(selected_user, df)
        with col1:
            fig, ax = plt.subplots()
            ax.barh(busy_day.index, busy_day.values)
            st.pyplot(fig)
        with col2:
            d = pd.DataFrame()
            d['Days'] = list(busy_day.index)
            d['Message Count'] = list(busy_day.values)
            st.dataframe(d)
#
# # ======================================================================================================================
# #
        # activity map
        st.markdown("<h2 style='text-align: left; color: yellow;'>Most busy month</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        busy_day = Helper.month_activity_map(selected_user, df)
        with col1:
            fig, ax = plt.subplots()
            ax.barh(busy_day.index, busy_day.values)
            st.pyplot(fig)
        with col2:
            d = pd.DataFrame()
            d['Months'] = list(busy_day.index)
            d['Message Count'] = list(busy_day.values)
            st.dataframe(d)

# # ======================================================================================================================

        # Weekly activity map
        st.markdown("<h2 style='text-align: left; color: yellow;'>Weekly activity map</h2>", unsafe_allow_html=True)
        pivot_table = Helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        # sns.set(rc={'figure.figsize': (15, 8)})
        ax = sns.heatmap(pivot_table)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
# #
# # ======================================================================================================================
#
        # find the busiest user in the group
        if selected_user == 'Overall':
            st.markdown("<h2 style='text-align: left; color: yellow;'>Most busy user</h2>", unsafe_allow_html=True)
            x, d = Helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='violet')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(d)
#
# # ======================================================================================================================
#
        # world cloud
        st.markdown("<h2 style='text-align: left; color: yellow;'>WordCloud</h2>", unsafe_allow_html=True)
        df_wc = Helper.create_wordcloud(selected_user, df)

        if df_wc is not None:
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)
        else:
            st.markdown("<h5 style='text-align: left; color: white;'>Not found</h5>", unsafe_allow_html=True)

# # ======================================================================================================================
#
        # most Common words
        st.markdown("<h2 style='text-align: left; color: yellow;'>Most Common Words</h2>", unsafe_allow_html=True)
        most_common_df = Helper.most_common_words(selected_user, df)

        col1, col2 = st.columns(2)

        if most_common_df is not None:
            with col1:
                fig, ax = plt.subplots()
                ax.barh(most_common_df['Words'], most_common_df['Count'])
                # plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(most_common_df)
        else:
            st.markdown("<h5 style='text-align: left; color: white;'>Not found</h5>", unsafe_allow_html=True)

# # ======================================================================================================================

        # emoji analysis
        st.markdown("<h2 style='text-align: left; color: yellow;'>Emoji Analysis</h2>", unsafe_allow_html=True)
        emoji_df = Helper.emoji_analysis(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            if emoji_df.shape[0] > 0:
                fig, ax = plt.subplots()
                myexplode = [0.1, 0.1, 0.2, 0.2, 0.2]

                ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emojis'].head(), explode=myexplode, autopct='%0.2f', shadow=True)
                st.pyplot(fig)
# # ======================================================================================================================
