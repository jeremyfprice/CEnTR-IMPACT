import streamlit as st
from time import sleep
def app():
    st.title('Check and Generate Scores')

    st.header("Check Your Existing Scores")
    have_id = st.radio("Do you have a unique ID from a previous survey?", ('Yes', 'No'))

    if have_id == 'Yes':
        unique_id = st.text_input("Please enter your unique ID:")
        if st.button('Retrieve Scores'):
            # Placeholder for the logic to retrieve and display scores based on the unique ID
            st.write("Scores for ID:", unique_id)
            # Actual implementation would involve fetching data from a database or server

    st.header("Want to know your score?")
    want_score = st.radio("Would you like to calculate your score now?", ('Yes', 'No'))

    if want_score == 'Yes':
        st.write("Please proceed to the survey page to fill out your details and calculate your scores.")
        if st.button("Go to Survey"):
            st.write("Redirecting to the survey page...")
            sleep(1)
            st.switch_page("pages/survey.py")
            # This button ideally would redirect to the survey page, but Streamlit does not support
            # page redirections directly. Instead, instruct the user how to navigate.
            # If using a multi-page setup, you might be able to manage navigation via session state or similar approach

if __name__ == "__main__":
    app()
