import os
import json
from dotenv import load_dotenv
from neo4j import GraphDatabase
import streamlit as st
from utils.unique_id import generate_unique_id
from opencage.geocoder import OpenCageGeocode, RateLimitExceededError
import pyperclip

# Load environment variables from .env file
load_dotenv()

# Get the values from environment variables
api_key = os.getenv('OPEN_CAGE_API_KEY')
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASSWORD')

geocoder = OpenCageGeocode(api_key)
driver = GraphDatabase.driver(uri, auth=(user, password))

def create_project_in_db(tx, project_data):
    query = """
    CREATE (project:Project {
        title: $title, 
        projectID: $projectID,
        startDate: $startDate, 
        endDate: $endDate, 
        location: $location, 
        latitude: $latitude, 
        longitude: $longitude, 
        leadership: $leadership
    })
    """
    tx.run(query, **project_data)

def app():
    st.title("Create Project and Initiate Survey")

    if 'projectID' not in st.session_state:
        st.session_state.projectID = generate_unique_id(12)

    # Initialize session state variables for this page if not already set
    if 'project_name' not in st.session_state:
        st.session_state.project_name = ''
    if 'location' not in st.session_state:
        st.session_state.location = ''
    if 'start_date' not in st.session_state:
        st.session_state.start_date = None
    if 'end_date' not in st.session_state:
        st.session_state.end_date = None
    if 'leadership' not in st.session_state:
        st.session_state.leadership = [{}]

    project_data = {
        "title": st.text_input("Project Title", st.session_state.project_name),
        "projectID": st.session_state.projectID,
        "location": st.text_input("Project Location (be as specific as possible based on the scale of the project)", st.session_state.location),
        "startDate": st.date_input("Approximate Project Start Date", st.session_state.start_date),
        "endDate": st.date_input("Approximate Project End Date (Leave blank if ongoing)", st.session_state.end_date),
        "latitude": None,
        "longitude": None,
        "leadership": st.session_state.leadership
    }

    if project_data["location"]:
        try:
            result = geocoder.geocode(project_data["location"])
            if result and len(result):
                project_data["latitude"] = result[0]['geometry']['lat']
                project_data["longitude"] = result[0]['geometry']['lng']
            else:
                st.error("Location not found. Please enter a valid location.")
        except RateLimitExceededError:
            st.error("Rate limit exceeded. Please try again later.")
        except Exception as e:
            st.error(f"Geocoding service error: {e}. Please try again later.")
    
    st.subheader("Project Leadership")
    num_leaders = len(st.session_state.leadership)
    for i in range(num_leaders):
        leader = st.session_state.leadership[i]
        leader["role"] = st.text_input(f"Role {i + 1}", key=f"role_{i}", value=leader.get("role", ""))
        leader["name"] = st.text_input(f"Name {i + 1}", key=f"name_{i}", value=leader.get("name", ""))
        leader["affiliation"] = st.text_input(f"Affiliation {i + 1}", key=f"affiliation_{i}", value=leader.get("affiliation", ""))

    if st.button("Add another leader"):
        st.session_state.leadership.append({})
        st.experimental_rerun()

    if st.button("Save Project and Initiate Survey"):
        # Check if all required fields are filled
        if not project_data["title"] or not project_data["location"] or not project_data["startDate"] or not any(leader.values() for leader in st.session_state.leadership):
            st.error("Please fill in all the fields before proceeding.")
        else:
            # Serialize the leadership data to JSON
            project_data["leadership"] = json.dumps(project_data["leadership"])
            with driver.session() as session:
                session.execute_write(create_project_in_db, project_data)
            st.success("Project data saved successfully!")
            st.write("Your Unique Project ID:", st.session_state.projectID)
            st.warning("Please save this ID for future reference.")
            
            # Create shareable link
            survey_link = f"http://localhost:8503/survey_page?id={st.session_state.projectID}"
            st.session_state.survey_link = survey_link

    if 'survey_link' in st.session_state:
        st.write("Shareable Link:", st.session_state.survey_link)
        if st.button("Copy Link"):
            pyperclip.copy(st.session_state.survey_link)
            st.success("Link copied to clipboard!")
        
        # Button to go to the survey page
        st.markdown(f"""
            <a href="{st.session_state.survey_link}" target="_self">
                <button style="padding: 0.5em; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    Go to Survey Form
                </button>
            </a>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
