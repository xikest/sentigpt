
from functions_text import *
from functions_timeseries import *
def main():
    # basic setting
    st.set_page_config(
        page_title="plot stream",
        layout="wide")

    # session state initialize
    st.session_state.setdefault("tab1", None)
    st.session_state.setdefault("tab2", None)
    st.session_state.setdefault("tab3", None)

    # Title
    st.header("Plot Visualization")

    # Side bar
    with st.sidebar:
        # Basic description
        st.subheader("Project Description")
        st.write("This project supports basic text analysis.")
        st.markdown("---")

        with st.expander("Usage", expanded=True):
            st.markdown("**1. Data Preparation**")
            st.write("- Upload a CSV or Excel file containing text data.")

            st.markdown("**2. Analysis Results**")
            st.write("- Review data summaries, including the most frequent words.")
            st.write("- Download word frequency analysis results as a CSV file.")

            st.markdown("**3. Visualization**")
            st.write("- Visualize top words and their frequencies in a bar chart.")
            st.write("- Generate word frequency in graphic format using a word cloud.")
            st.write("- Create a network graph of topics and related words using LDA.")

        st.markdown("---")
        st.write(
            """     
            Written by TJ.Kim ☕
            """
        )
        st.markdown("---")

    # Insert containers separated into tabs:
    tab1, tab2, tab3 = st.tabs(["Text Analysis", "Time Series Analysis", "Numeric Analysis"])

    with tab1:
        col1_tab1, col2_tab1 = st.columns([1, 2])
        with col1_tab1:
            st.subheader("1. Data Preparation")
            df_example = call_example_comments()
            download_df_as_csv(df_example, file_name="example_text_data", key="download_csv_text_example", label="Sample")
            text_data_uploaded = st.file_uploader("Upload Text data", key="time_text_data")
            if text_data_uploaded is not None:
                try:
                    comments = read_comments_from(text_data_uploaded, column_name="comments")
                    comments_as_string = ' '.join(comments.astype(str))
                    nouns = prepare_nouns(comments)
                    df_word_freq = prepare_word_freq(nouns)
                    corpus, dictionary = prepare_networkg(comments_as_string)

                    st.session_state["tab1"] = {"plot_df_word_freq": df_word_freq,
                                                "wordcloud_nouns": nouns,
                                                "network_corpus":corpus,
                                                "network_dictionary":dictionary}
                    st.subheader("2. Analysis results")
                    # download btn
                    download_df_as_csv(df_word_freq, file_name="word_freq_analysis", key="download_csv_text_analysis", label="Result")
                except:
                    st.error('Please verify the file format', icon="🚨")
        with col2_tab1:
            if st.session_state["tab1"] is not None:
                st.subheader("3. Visualization")
                tab1_col2_tab1, tab2_col2_tab1, tab3_col2_tab1 = st.tabs(["Plot", "Word Cloud", "Network Graph"])
                with tab1_col2_tab1:
                    df_word_freq = st.session_state["tab1"]["plot_df_word_freq"]
                    plot_freq(df_word_freq)
                with tab2_col2_tab1:
                    nouns = st.session_state["tab1"]["wordcloud_nouns"]
                    plot_wordcloud(nouns)
                with tab3_col2_tab1:
                    corpus = st.session_state["tab1"]["network_corpus"]
                    dictionary = st.session_state["tab1"]["network_dictionary"]
                    plot_networkg(corpus, dictionary)
    with tab2:
        col1_tab3, col2_tab3 = st.columns([1, 2])
        with col1_tab3:
            st.subheader("1. Data Preparation")
            df_example = call_example_timeseries()
            download_df_as_csv(df_example, "example_timeseries_data", key="download_csv_timeseries_example", label="Sample")
            time_data_uploaded = st.file_uploader("Upload Time Series", key="time_series_uploader")
            if time_data_uploaded is not None:
                try:
                    timeseries = read_timeseries_from(time_data_uploaded)
                    st.session_state["tab3"] = {"timeseries": timeseries}
                    plot_time_series(timeseries)
                except:
                    st.error('Please verify the file format', icon="🚨")
        with col2_tab3:
            if st.session_state["tab3"] is not None:
                st.subheader("2. Visualization")
                tab1_col2_tab3, tab2_col2_tab3  = st.tabs(["TimeSeries", "Prophet Plot"])
                timeseries = st.session_state["tab3"]["timeseries"]
                with tab1_col2_tab3:
                    plot_decompose_timeseries(timeseries)

                with tab2_col2_tab3:
                    plot_prophet(timeseries)




    with tab3:
        st.subheader("In the conceptualization stage")

if __name__ == "__main__":
    main()