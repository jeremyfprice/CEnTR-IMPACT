import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import streamlit as st
from utils.unique_id import generate_unique_id
from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import RateLimitExceededError
from streamlit_sortables import sort_items
import json

# Load environment variables from .env file
load_dotenv()

# Get the values from environment variables
api_key = os.getenv('OPEN_CAGE_API_KEY')
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASSWORD')

geocoder = OpenCageGeocode(api_key)
driver = GraphDatabase.driver(uri, auth=(user, password))

def create_survey_in_db(tx, preferences):
    query = """
    CREATE (temp_pref:TempPreference {
        unique_id: $unique_id, 
        project_name: $project_name, 
        researcher_name: $researcher_name,
        start_date: $start_date,
        end_date: $end_date,
        location: $location,
        latitude: $latitude,
        longitude: $longitude,
        leadership: $leadership,
        partners: $partners,
        challenges_goals: $challenges_goals,
        sectors: $sectors,
        score_visualizations: $score_visualizations,
        direct_indicator_preferences: $direct_indicator_preferences,
        challenge_origin: $challenge_origin,
        diversity: $diversity,
        resources: $resources,
        beneficence: $beneficence,
        reflection: $reflection,
        decision_making: $decision_making,
        tool_construction: $tool_construction
    })
    RETURN temp_pref
    """
    # Serialize the complex structures to JSON strings
    preferences['leadership'] = json.dumps(preferences['leadership'])
    preferences['partners'] = json.dumps(preferences['partners'])
    preferences['score_visualizations'] = json.dumps(preferences['score_visualizations'])
    preferences['direct_indicator_preferences'] = json.dumps(preferences['direct_indicator_preferences'])
    preferences['challenge_origin'] = json.dumps(preferences['challenge_origin'])
    preferences['diversity'] = json.dumps(preferences['diversity'])
    preferences['resources'] = json.dumps(preferences['resources'])
    preferences['beneficence'] = json.dumps(preferences['beneficence'])
    preferences['reflection'] = json.dumps(preferences['reflection'])
    preferences['decision_making'] = json.dumps(preferences['decision_making'])
    preferences['tool_construction'] = json.dumps(preferences['tool_construction'])

    tx.run(query, **preferences)

def page_1():
    st.title("Initiate Project Alignment Survey - Page 1")

    if 'leadership' not in st.session_state:
        st.session_state.leadership = [{}]

    unique_id_option = st.radio("Do you have a unique ID?", ("No", "Yes"))

    next_page = None
    submit_form = None

    with st.form("page_1"):
        st.session_state.project_name = st.text_input("Project Name", st.session_state.get('project_name', ''))
        st.session_state.researcher_name = st.text_input("Researcher Name", st.session_state.get('researcher_name', ''))
        
        if unique_id_option == "Yes":
            st.session_state.unique_id = st.text_input("Please enter your unique ID:")
        else:
            st.session_state.unique_id = generate_unique_id(16)
            st.write("Your Unique Survey ID:", st.session_state.unique_id)
            st.write("Please save this ID for future reference.")
        
        st.session_state.start_date = st.date_input("Approximate Project Start Date", st.session_state.get('start_date', None))
        st.session_state.end_date = st.date_input("Approximate Project End Date (leave blank if ongoing)", st.session_state.get('end_date', None))

        st.session_state.location_text = st.text_input("Project Location", st.session_state.get('location_text', ''))
        latitude = None
        longitude = None
        if st.session_state.location_text:
            try:
                result = geocoder.geocode(st.session_state.location_text)
                if result and len(result):
                    latitude = result[0]['geometry']['lat']
                    longitude = result[0]['geometry']['lng']
                    st.write(f"Latitude: {latitude}, Longitude: {longitude}")
                    st.session_state.latitude = latitude
                    st.session_state.longitude = longitude
                else:
                    st.error("Location not found. Please enter a valid location.")
            except RateLimitExceededError:
                st.error("Rate limit exceeded. Please try again later.")
            except Exception as e:
                st.error(f"Geocoding service error: {e}. Please try again later.")
        
        st.subheader("Project Leadership")
        num_leaders = len(st.session_state.leadership)
        for i in range(num_leaders):
            st.session_state.leadership[i]['role'] = st.text_input(f"Role {i + 1}", key=f"role_{i}", value=st.session_state.leadership[i].get('role', ''), label_visibility="collapsed")
            st.session_state.leadership[i]['name'] = st.text_input(f"Name {i + 1}", key=f"name_{i}", value=st.session_state.leadership[i].get('name', ''), label_visibility="collapsed")
            st.session_state.leadership[i]['affiliation'] = st.text_input(f"Affiliation {i + 1}", key=f"affiliation_{i}", value=st.session_state.leadership[i].get('affiliation', ''), label_visibility="collapsed")

        add_leader = st.form_submit_button("Add another leader")
        if add_leader:
            st.session_state.leadership.append({})

        st.subheader("Community Institutional Partners")
        st.session_state.partners = st.multiselect("Select Partners", ["Profit", "Non-Profit", "Agencies", "Grassroot Networks", "Other"], default=st.session_state.get('partners', []))
        if "Other" in st.session_state.partners:
            st.session_state.other_partners = st.text_input("Please specify other partners", st.session_state.get('other_partners', ''))

        st.session_state.challenges_goals = st.text_input("Project Challenges and/or Goals", st.session_state.get('challenges_goals', ''))

        st.session_state.sectors = st.multiselect("Project Sector(s)", [
            "Public Health and Wellness", "Education and Social Services", "Policy, Governance, and Justice",
            "Environment and Ecological Resilience", "Food and Nutritional Access", "Workforce Development and Entrepreneurship"
        ], default=st.session_state.get('sectors', []))

        st.subheader("Score Visualizations")
        st.session_state.selected_scores = st.multiselect("Select Score Visualizations (Alignment and Ripple Effect scores are required)", [
            "Direct Indicators Scores", "Project Impact Scores", "Alignment Scores", "Ripple Effect Scores"
        ], default=st.session_state.get('selected_scores', ["Alignment Scores", "Ripple Effect Scores"]))

        st.session_state.direct_indicator_preferences = {}
        if "Direct Indicators Scores" in st.session_state.selected_scores:
            st.subheader("Direct Indicator Preferences")
            st.session_state.direct_indicator_preferences["Community Partners"] = st.number_input("Community Partners", min_value=0, value=st.session_state.direct_indicator_preferences.get("Community Partners", 0))
            st.session_state.direct_indicator_preferences["Engagement Hours"] = st.number_input("Engagement Hours", min_value=0, value=st.session_state.direct_indicator_preferences.get("Engagement Hours", 0))
            st.session_state.direct_indicator_preferences["Individuals Served"] = st.number_input("Individuals Served", min_value=0, value=st.session_state.direct_indicator_preferences.get("Individuals Served", 0))
            st.session_state.direct_indicator_preferences["Infrastructure Tools"] = st.number_input("Infrastructure Tools", min_value=0, value=st.session_state.direct_indicator_preferences.get("Infrastructure Tools", 0))
            st.session_state.direct_indicator_preferences["Output Products"] = st.number_input("Output Products", min_value=0, value=st.session_state.direct_indicator_preferences.get("Output Products", 0))
            st.session_state.direct_indicator_preferences["Students Involved"] = st.number_input("Students Involved", min_value=0, value=st.session_state.direct_indicator_preferences.get("Students Involved", 0))
            st.session_state.direct_indicator_preferences["Successful Outcomes"] = st.number_input("Successful Outcomes", min_value=0, value=st.session_state.direct_indicator_preferences.get("Successful Outcomes", 0))

        if "Project Impact Scores" in st.session_state.selected_scores:
            next_page = st.form_submit_button("Next")
        else:
            submit_form = st.form_submit_button("Submit")

    if next_page:
        st.session_state.page = 2

    if submit_form:
        preferences = {
            "unique_id": st.session_state.unique_id,
            "project_name": st.session_state.project_name,
            "researcher_name": st.session_state.researcher_name,
            "start_date": st.session_state.start_date.strftime("%Y-%m-%d") if st.session_state.start_date else None,
            "end_date": st.session_state.end_date.strftime("%Y-%m-%d") if st.session_state.end_date else None,
            "location": st.session_state.location_text,
            "latitude": st.session_state.latitude,
            "longitude": st.session_state.longitude,
            "leadership": st.session_state.leadership,
            "partners": st.session_state.partners,
            "challenges_goals": st.session_state.challenges_goals,
            "sectors": st.session_state.sectors,
            "score_visualizations": st.session_state.selected_scores,
            "direct_indicator_preferences": st.session_state.direct_indicator_preferences
        }

        # Serialize the complex structures to JSON strings
        preferences['leadership'] = json.dumps(preferences['leadership'])
        preferences['partners'] = json.dumps(preferences['partners'])
        preferences['score_visualizations'] = json.dumps(preferences['score_visualizations'])
        preferences['direct_indicator_preferences'] = json.dumps(preferences['direct_indicator_preferences'])

        with driver.session() as session:
            session.execute_write(create_survey_in_db, preferences)

        st.success("Survey Created Successfully!")
        survey_link = f"http://localhost:8504/survey_page?id={st.session_state.unique_id}"
        st.write("Your Unique Survey ID:", st.session_state.unique_id)
        st.write("Shareable Link:", survey_link)

def page_2():
    import streamlit as st
    from streamlit_sortables import sort_items

    st.title("Initiate Project Alignment Survey - Page 2")

    # Project Impact Scores
    st.subheader("Project Impact Scores")
    
    # Challenge Origin
    st.subheader("Challenge Origin")
    challenge_origin_items = [
        "Entirely from the Research Team",
        "Identified by the Community, Refined and Defined by the Research Team",
        "Negotiated Fairly Equally between the Research Team and the Community",
        "Identified by the Research Team, Refined and Defined by the Community",
        "Entirely from the Community"
    ]
    challenge_origin = sort_items([
        {'header': 'Does Not Describe My Project', 'items': challenge_origin_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")

    # Diversity
    st.subheader("Diversity")
    diversity_items = [
        "The Research Team is diverse in multiple ways and represents a range of identities.",
        "The Community is diverse in multiple ways and represents a range of identities.",
        "Underrepresented and/or marginalized identities are a part of the Research Team.",
        "Underrepresented and/or marginalized identities are a part of the Community.",
        "The Research Team is homogenous and does not represent a range of identities.",
        "The Community is homogenous and does not represent a range of identities."
    ]
    diversity = sort_items([
        {'header': 'Does Not Describe My Project', 'items': diversity_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")

    # Resources
    st.subheader("Resources")
    resources_items = [
        "Entirely from the Research Team (1)",
        "Mostly from the Research Team, some from the Community.",
        "Equally between the Research Team and the Community.",
        "Mostly from the Community, some from the Research Team.",
        "Entirely from the Community (0.9)"
    ]
    resources = sort_items([
        {'header': 'Does Not Describe My Project', 'items': resources_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")

    # Beneficence
    st.subheader("Beneficence")
    beneficence_items = [
        "Entirely for the Research Team",
        "Mostly for the Research Team, some for the Community",
        "Equally for the Research Team and the Community",
        "Mostly for the Community, some for the Research Team",
        "Entirely for the Community"
    ]
    beneficence = sort_items([
        {'header': 'Does Not Describe My Project', 'items': beneficence_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")

    # Reflection
    st.subheader("Reflection")
    reflection_items = [
        "The Research Team engaged in and benefitted from reflection and reflexivity activities.",
        "Community partners engaged in and benefitted from reflection and reflexivity activities.",
        "The Research Team and Community partners collaboratively planned reflection and reflexivity activities.",
        "Lessons learned for all participants were identified through reflection and reflexivity activities.",
        "Strategies and new practices were identified through reflection and reflexivity activities."
    ]
    reflection = sort_items([
        {'header': 'Does Not Describe My Project', 'items': reflection_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")

    # Decision Making
    st.subheader("Decision Making")
    decision_making_items = [
        "The Research Team contributed to the decision making processes",
        "Community Partners contributed to the decision making processes",
        "Decision making was conducted through clear and understood processes",
        "Decision making processes recognized and supported the community’s cultural capital and agency",
        "Decisions were made to align with the goals and purposes of the project"
    ]
    decision_making = sort_items([
        {'header': 'Does Not Describe My Project', 'items': decision_making_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")

    # Tool Construction
    st.subheader("Tool Construction")
    tool_construction_items = [
        "Promotes Efficiency Only",
        "Promotes Predominantly Efficiency And Recognizes Honor, Plurality, and Multivocality",
        "Promotes Efficiency, Plurality, Multivocality, and Honor Equitably",
        "Promotes Predominantly Honor, Plurality, and Multivocality And Efficiency",
        "Promotes Predominantly Honor, Plurality, and Multivocality Only"
    ]
    tool_construction = sort_items([
        {'header': 'Does Not Describe My Project', 'items': tool_construction_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")

    # Navigation buttons
    if st.button("Previous"):
        st.session_state.page = 1

    # Adding CSS to style the submit button
    st.markdown("""
    <style>
    #submit-button button {
        padding: 20px;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    submitted = st.button("Submit", key='submit-button')
    if submitted:
        preferences = {
            "unique_id": st.session_state.unique_id,
            "project_name": st.session_state.project_name,
            "researcher_name": st.session_state.researcher_name,
            "start_date": st.session_state.start_date.strftime("%Y-%m-%d") if st.session_state.start_date else None,
            "end_date": st.session_state.end_date.strftime("%Y-%m-%d") if st.session_state.end_date else None,
            "location": st.session_state.location_text,
            "latitude": st.session_state.latitude,
            "longitude": st.session_state.longitude,
            "leadership": st.session_state.leadership,
            "partners": st.session_state.partners,
            "challenges_goals": st.session_state.challenges_goals,
            "sectors": st.session_state.sectors,
            "score_visualizations": st.session_state.selected_scores,
            "direct_indicator_preferences": st.session_state.direct_indicator_preferences,
            "challenge_origin": challenge_origin,
            "diversity": diversity,
            "resources": resources,
            "beneficence": beneficence,
            "reflection": reflection,
            "decision_making": decision_making,
            "tool_construction": tool_construction
        }

        # Serialize the complex structures to JSON strings
        preferences['leadership'] = json.dumps(preferences['leadership'])
        preferences['partners'] = json.dumps(preferences['partners'])
        preferences['score_visualizations'] = json.dumps(preferences['score_visualizations'])
        preferences['direct_indicator_preferences'] = json.dumps(preferences['direct_indicator_preferences'])
        preferences['challenge_origin'] = json.dumps(preferences['challenge_origin'])
        preferences['diversity'] = json.dumps(preferences['diversity'])
        preferences['resources'] = json.dumps(preferences['resources'])
        preferences['beneficence'] = json.dumps(preferences['beneficence'])
        preferences['reflection'] = json.dumps(preferences['reflection'])
        preferences['decision_making'] = json.dumps(preferences['decision_making'])
        preferences['tool_construction'] = json.dumps(preferences['tool_construction'])

        with driver.session() as session:
            session.execute_write(create_survey_in_db, preferences)

        st.success("Survey Created Successfully!")
        survey_link = f"http://localhost:8504/survey_page?id={st.session_state.unique_id}"
        st.write("Your Unique Survey ID:", st.session_state.unique_id)
        st.write("Shareable Link:", survey_link)

def app():
    if 'page' not in st.session_state:
        st.session_state.page = 1

    if st.session_state.page == 1:
        page_1()
    elif st.session_state.page == 2:
        page_2()

if __name__ == "__main__":
    app()
