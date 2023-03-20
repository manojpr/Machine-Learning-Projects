import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp chat analyszer")

upload_file=st.sidebar.file_uploader("Choose a File")
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data = bytes_data.decode('utf-8')
    df=preprocessor.preprocessing(data)
    st.dataframe(df)
    #fetch unique user
    user_list=df['User'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"All")
    selected_user=st.sidebar.selectbox("Show analysis with respect to ",user_list)

    if st.sidebar.button("Show analysis"):
        num_messages,words,media,link=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(media)
        with col4:
            st.header("Link shared")
            st.title(link)

        if selected_user=='All':
            st.header("Most active user")
            x,n_df=helper.most_busy(df)
            fig,ax=plt.subplots()
            
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(n_df)
            #wordcloud
        st.title("Insights")
        st.header('Message Frequency')
        if selected_user=='All':
            timeline=helper.frequency(df)
        else:
            timeline=helper.frequency(df,selected_user)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'][-25:],timeline['Messages'][-25:],color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        #most_common
        
        st.header("Most frequently used words")
        col1,col2=st.columns(2)
        if selected_user=='All':
            m_df=helper.most_common(df)
        else:
            m_df=helper.most_common(df,selected_user)
        
        with col1:
            fig,ax=plt.subplots()
            ax.bar(m_df['words'],m_df['count'])
            plt.xticks(rotation='vertical')
            
            st.pyplot(fig)
        with col2:
            st.dataframe(m_df)
        # emoji counter (missing)

        st.header("Monthly and daily message frequency")
        col1,col2=st.columns(2)
        if selected_user=='All':
            m_df=helper.monthly_freq(df)
        else:
            m_df=helper.monthly_freq(df,selected_user)
        
        with col1:
            fig,ax=plt.subplots()
            ax.bar(m_df['month'],m_df['Messages'],color='orange')
            plt.xticks(rotation=90)
            
            st.pyplot(fig)
        with col2:
            if selected_user=='All':
                m_df=helper.day_freq(df)
            else:
                m_df=helper.day_freq(df,selected_user)
            fig,ax=plt.subplots()
            ax.bar(m_df['Day_name'],m_df['Messages'],color='green')
            plt.xticks(rotation=90)
            st.pyplot(fig)