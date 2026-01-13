import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager as fm

# Load Windows emoji font
emoji_font = fm.FontProperties(fname=r"C:\Windows\Fonts\seguiemj.ttf")

# Streamlit config
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
st.sidebar.title("📊 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload WhatsApp chat (.txt)", type=["txt"])

if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8", errors="ignore")

    st.subheader("📄 Chat File Preview")
    st.code(data[:600] + "\n...\n(file trimmed for preview)")

    df = preprocessor.preprocess(data)

    st.subheader("🧾 Processed DataFrame")

    if df is None:
        st.error("❌ preprocess() returned None!")
    elif df.empty:
        st.warning("⚠ Chat could not be parsed — check export format.")
    else:
        st.success("✔ Data loaded successfully!")
        st.dataframe(df, use_container_width=True)

        user_list = df['user'].unique().tolist()
        if "group_notification" in user_list:
            user_list.remove("group_notification")
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("Analyze chat for", user_list)

        if st.sidebar.button("📊 Show Analysis"):

            # 1 =====================================================
            st.title("📌 Overall Chat Statistics")
            num_messages, words, media, links = helper.fetch_stats(selected_user, df)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Messages", num_messages)
            col2.metric("Words", words)
            col3.metric("Media Shared", media)
            col4.metric("Links", links)

            # 2 =====================================================
            st.title("📅 Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)

            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], marker='o')
            plt.xticks(rotation=90)
            st.pyplot(fig)

            # 3 =====================================================
            st.title("📆 Daily Timeline")
            daily = helper.daily_timeline(selected_user, df)

            fig, ax = plt.subplots()
            ax.plot(daily['only_date'], daily['message'], marker='o', linewidth=2)
            plt.xticks(rotation=90)
            st.pyplot(fig)

            # 4 🔥 HEATMAP =================================================
            st.title("🟩 Weekly × Hourly Activity Heatmap")

            heatmap = helper.activity_heatmap(selected_user, df)

            fig, ax = plt.subplots(figsize=(12, 4))
            sns.heatmap(heatmap, cmap="Greens", linewidths=.5, annot=False)
            plt.ylabel("Day")
            plt.xlabel("Hour Period")
            st.pyplot(fig)

            # 5 =====================================================
            if selected_user == "Overall":
                st.title("🔥 Most Active Users")
                x, new_df = helper.most_busy_users(df)

                col1, col2 = st.columns(2)

                with col1:
                    fig, ax = plt.subplots()
                    ax.bar(x.index, x.values)
                    plt.xticks(rotation=90)
                    st.pyplot(fig)

                with col2:
                    st.dataframe(new_df)

            # 6 =====================================================
            st.title("☁ Word Cloud")
            wc_img = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(wc_img)
            ax.axis("off")
            st.pyplot(fig)

            # 7 =====================================================
            st.title("🔤 Most Common Words")
            most_common_df = helper.most_common_words(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(most_common_df['word'], most_common_df['count'])
            plt.xticks(rotation=90)
            st.pyplot(fig)

            st.dataframe(most_common_df)

            # 8 =====================================================
            st.title("😀 Emoji Usage Analysis")
            emoji_df = helper.emoji_helper(selected_user, df)

            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)

            with col2:
                top_10 = emoji_df.head(10)
                fig, ax = plt.subplots()
                wedges, texts, autotexts = ax.pie(
                    top_10['count'], labels=top_10['emoji'],
                    autopct='%1.1f%%',
                    textprops={'fontproperties': emoji_font, 'fontsize': 14}
                )
                for text in texts:
                    text.set_fontproperties(emoji_font)
                st.pyplot(fig)
