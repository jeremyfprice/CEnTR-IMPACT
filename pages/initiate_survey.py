# import os
# from dotenv import load_dotenv
# from neo4j import GraphDatabase
# import streamlit as st
# from utils.unique_id import generate_unique_id
# import pyperclip

# # Load environment variables from .env file
# load_dotenv()

# # Get the values from environment variables
# uri = os.getenv('NEO4J_URI')
# user = os.getenv('NEO4J_USER')
# password = os.getenv('NEO4J_PASSWORD')

# driver = GraphDatabase.driver(uri, auth=(user, password))

# def app():
#     st.title("Survey Creation")

#     if 'unique_id' not in st.session_state:
#         st.session_state.unique_id = None

#     unique_id_option = st.radio("Do you have a unique ID?", ("No", "Yes"))

#     if unique_id_option == "Yes":
#         st.session_state.unique_id = st.text_input("Please enter your unique ID:")
#         if st.button("Continue"):
#             if st.session_state.unique_id:
#                 survey_link = f"http://localhost/survey_page?id={st.session_state.unique_id}"
#                 st.session_state.survey_link = survey_link
#                 st.rerun()
#             else:
#                 st.error("Please enter a unique ID to continue.")
#     else:
#         if not st.session_state.unique_id:
#             st.session_state.unique_id = generate_unique_id(12)
#         st.write("Your Unique Survey ID:", st.session_state.unique_id)
#         st.write("Please save this ID for future reference.")

        # if st.button("Create Survey"):
        #     survey_link = f"http://localhost/survey_page?id={st.session_state.unique_id}"
        #     st.session_state.survey_link = survey_link
        #     st.rerun()

#     if 'survey_link' in st.session_state:
#         st.write("Shareable Link:", f"[{st.session_state.survey_link}]({st.session_state.survey_link})")
        
#         if st.button("Copy Link"):
#             pyperclip.copy(st.session_state.survey_link)
#             st.success("Link copied to clipboard!")
        
#         st.markdown(f"""
#             <a href="{st.session_state.survey_link}" target="_self">
#                 <button style="padding: 0.5em; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
#                     Go to Survey Page
#                 </button>
#             </a>
#             """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     app()
