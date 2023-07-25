import streamlit as st
from streamlit_option_menu import option_menu
import webbrowser
import preprocessor
import helpers
import matplotlib.pyplot as plt
import seaborn as sns


# st.sidebar.title("Chat Analyzer Primary version")

def uploadFile(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.header('Great ! Now click on the "Show Analysis" button')
    # fetch unique users
    user_list = df['user'].unique().tolist()

    for x in user_list:
        if x == 'group_notification':
            user_list.remove('group_notification')
            break
    # sort the user_list in accending order of names
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show analysis"):
        # Statistics Area starts

        num_messages, words, num_media_messages, num_links = helpers.fetch_stats(
            selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # finding the most active users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helpers.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud provides the representation all the words with different font size
        st.title("Wordcloud")
        df_wc = helpers.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words

        most_common_df = helpers.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helpers.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),
                   labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helpers.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helpers.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],
                daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helpers.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helpers.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        # heatmap of activity
        st.title("Weekly Activity Map")
        user_heatmap = helpers.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


def main():
    # Set the page configuration and layout
    st.set_page_config(
        page_title="Chat Analyzer",
        layout="wide",
        initial_sidebar_state="auto",
    )
    # Create a sidebar with option_menu
    logo_image = "./media/logos/logo1.png"
    st.sidebar.image(logo_image,
                     width=300)
    padding_top = -30

    with st.sidebar:
        selected = option_menu("Chat Analysis", ["Home", "Get started", "Project Demo", "Generate Reports"], icons=[
            'house', 'play-btn', 'github', 'graph-up-arrow'], menu_icon="cast", default_index=0)

    st.title('Simple Chat Analysis')

    # Add your logo on the top left in the sidebar

    custom_css = ''' 
    <style> 
    div.custom-container { 
        max-width: 800px;
        height:250px;
        font-size:14px;
    } 

    div.horizontal-buttons {
        display: flex;
        justify-content: center;
    }
    
    </style> 
    '''
    st.markdown(f"""
    <style>
        
        .reportview-container .main .block-container{{
            padding-top: {padding_top}rem;
        }}


    </style>""", unsafe_allow_html=True,)

    # The rest of your app content goes here

    # Create a grid layout with 2 columns
    col1, col2 = st.columns(2)

    # Load your images (replace these paths with your actual image file paths)
    image1 = "./media/background5.jpeg"
    image2 = "./media/background6.png"

    # Display images in the grid
    col1.image(image1, use_column_width=True, width=200)
    col2.image(image2, use_column_width=True, width=200)

    st.markdown(custom_css, unsafe_allow_html=True)

    # Add content inside the custom container
    st.markdown('<div class="custom-container"> <h3>Generate interactive, beautiful and insightful chat analysis reports </h3> <p> <strong>Introducing ChatAnalyzer</strong>- your <em>ultimate</em> <strong>companion</strong> in unraveling the secrets of <em>online chating!</em> With its cutting-edge <strong>analytics</strong>, dive into a world of <em>thrilling insights</em>. Uncover the #1 analysis, <strong>decode</strong> the most popular <strong>emojis</strong> within the group, and witness the <em>staggering message flow</em> each day. ChatAnalyzer: <em>where curiosity meets data, and the extraordinary journey of communication exploration begins!</em> </p>Everything is <strong>processed</strong> in your browser.🔒 No data leaves your device.Can handle <strong>millions</strong> of messages and multiple chats. Free and <strong>open source</strong> ❤️ </div>', unsafe_allow_html=True)

    st.markdown('<div > Supports: <img width="16" height="16" src="https://img.icons8.com/external-those-icons-flat-those-icons/24/external-WhatsApp-Logo-social-media-those-icons-flat-those-icons.png" alt="external-WhatsApp-Logo-social-media-those-icons-flat-those-icons"/> <img width="18" height="18" src="https://img.icons8.com/color/16/telegram-app--v1.png" alt="telegram-app--v1"/><img width="18" height="18" src="https://img.icons8.com/color/48/000000/discord--v2.png" alt="discord--v2"/>  <img width="18" height="18" src="https://img.icons8.com/color/48/facebook-messenger--v1.png" alt="facebook-messenger--v1"/></div>',
                unsafe_allow_html=True)
    # Close the custom container
    st.markdown('</div>', unsafe_allow_html=True)

    # Check if the button is clicked
    if selected == "Home":
        pass
    elif selected == "Get started":
        get_started()

    elif selected == "Project Demo":
        generate_demo()
    elif selected == "Generate Reports":
        generate_report()

    uploaded_file = st.file_uploader("Upload a file")

    with st.sidebar:
        selected = option_menu(None, ["Uploaded file analysis section"], icons=[
            'graph-up-arrow'], menu_icon="cast", orientation="horizontal")
        st.sidebar.markdown(
            '<img width="30" height="30" src="https://img.icons8.com/ios-filled/50/github.png" alt="github"/> **Project Repository:**  [click here](https://github.com/Pursottam6003/chat_analyzer)   ', unsafe_allow_html=True)

        st.sidebar.markdown(
            'Designed and _Developed by **Pursottam Sah**_ [src](https://linkedin.com/in/pursottamsah)', unsafe_allow_html=True)
    if uploaded_file:
        st.write("File Uploaded Successfully!")
        uploadFile(uploaded_file)


def generate_report():
    st.markdown(' 1. To generatea a report you should have a <kbd>.txt</kbd> file being exported via chat if not please click on <kbd>get started</kbd> button to learn more... ', unsafe_allow_html=True)
    st.markdown(
        '2. Click on the <kbd>browse file</kbd> option on the bottom of page and select the file.', unsafe_allow_html=True)
    st.markdown(
        '3. And then click <kbd>show analysis</kbd> button on the bottom of sidenav bar', unsafe_allow_html=True)
    st.markdown('4. There is one <kbd>dropdown</kbd> to select single user analysis ',
                unsafe_allow_html=True)


def generate_demo():
    # st.markdown('<img src="./media/demo.webm" alt="demo_video" />',
    #             unsafe_allow_html=True)
    st.markdown('<iframe width="560" height="315" src="https://www.youtube.com/embed/2bW4ZDqFVWc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
                unsafe_allow_html=True)


def get_started():
    st.markdown(
        '1. Go to **WhatsApp** in your mobile phone and select the **desired** group/person')
    st.markdown(
        '2. Press the context <kbd>**menu**</kbd> ( <img width="12" height="16" src="https://img.icons8.com/ios-filled/50/menu-2.png" alt="menu-2"/> ) in the top right corner', unsafe_allow_html=True)
    st.markdown('3. In the context menu, select the <kbd>**"More"**</kbd> item',
                unsafe_allow_html=True)
    st.image('./media/tut1.png', width=250)

    st.markdown('4. In the new menu, _choose_  <kbd>**"Export Chat"**</kbd>.',
                unsafe_allow_html=True)
    st.image('./media/tut2.jpeg', width=200)

    st.markdown('5. You should get a _popup_ where you need to choose between exporting with or without media. Choose the <kbd>**"Without Media"**</kbd> option.', unsafe_allow_html=True)
    st.image('./media/tut3.png', width=300)

    st.markdown('6. **Email** the **exported text** file to yourself.',
                unsafe_allow_html=True)
    st.image('./media/tut4.png', width=300)

    st.markdown(
        '7. **Download** the file to your computer, and <kbd>**upload**</kbd> it to _ChatAnalyzer_ ', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
