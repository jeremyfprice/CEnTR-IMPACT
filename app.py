import streamlit as st
from pages import homepage, survey_page, scores, visualizations, create_project_page

def setup_page():
    st.set_page_config(page_title="Homepage", layout='wide')
    st.markdown("""
        <style>
        .css-1aumxhk {  # Hide the sidebar
            display: none;
        }
        .reportview-container .main .block-container {
            padding-top: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
            padding-bottom: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)

def main():
    setup_page()
    query_params = st.query_params  # Use st.query_params to get query parameters
    page = query_params.get("page", ["Home"])[0]  # Default to Home if no page is specified
    survey_id = query_params.get("id", None)  # Check if there is an 'id' query parameter

    PAGES = {
        "Home": homepage,
        "Create Project": create_project_page,  # Add the new page here
        "Survey form": survey_page,
        "Generate Scores": scores,
        "Visualizations": visualizations
    }

    if survey_id:
        survey_page.app(survey_id[0])  # Assuming survey_page.app can handle an ID
    else:
        page_app = PAGES.get(page, homepage)
        page_app.app()

if __name__ == "__main__":
    main()
