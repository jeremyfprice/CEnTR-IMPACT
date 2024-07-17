import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import streamlit as st
from utils.unique_id import generate_unique_id
from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import RateLimitExceededError
from streamlit_sortables import sort_items
import json
from scipy.stats import gmean

# Load environment variables from .env file
load_dotenv()

# Get the values from environment variables
api_key = os.getenv('OPEN_CAGE_API_KEY')
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASSWORD')

geocoder = OpenCageGeocode(api_key)
driver = GraphDatabase.driver(uri, auth=(user, password))

multipliers = [
    (1, "(1)"),
    (0.95, "(0.95)"),
    (0.90, "(0.90)"),
    (0.84, "(0.84)"),
    (0.78, "(0.78)")
]

def check_unique_id(tx, projectID):
    query = "MATCH (project:Project {projectID: $projectID}) RETURN project"
    result = tx.run(query, projectID=projectID)
    return result.single() is not None

def calculate_sortable_score(items, multipliers):
    score = 0
    for i, item in enumerate(items):
        for weight, text in multipliers:
            if text in item:
                score += weight * (1 - 0.05 * i)
    return score / 4.027

def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 0
    if 'projectID' not in st.session_state:
        st.session_state.projectID = ''
    if 'project_name' not in st.session_state:
        st.session_state.project_name = ''
    if 'partners' not in st.session_state:
        st.session_state.partners = []
    if 'selected_scores' not in st.session_state:
        st.session_state.selected_scores = []
    if 'direct_indicator_preferences' not in st.session_state:
        st.session_state.direct_indicator_preferences = {}
    if 'challenge_origin_score' not in st.session_state:
        st.session_state.challenge_origin_score = 0
    if 'diversity_score' not in st.session_state:
        st.session_state.diversity_score = 0
    if 'resources_score' not in st.session_state:
        st.session_state.resources_score = 0
    if 'beneficence_score' not in st.session_state:
        st.session_state.beneficence_score = 0
    if 'reflection_score' not in st.session_state:
        st.session_state.reflection_score = 0
    if 'decision_making_score' not in st.session_state:
        st.session_state.decision_making_score = 0
    if 'tool_construction_score' not in st.session_state:
        st.session_state.tool_construction_score = 0
    if 'trust_score' not in st.session_state:
        st.session_state.trust_score = 0
    if 'duration_score' not in st.session_state:
        st.session_state.duration_score = 0
    if 'frequency_score' not in st.session_state:
        st.session_state.frequency_score = 0
    if 'research_questions_score' not in st.session_state:
        st.session_state.research_questions_score = 0
    if 'design_facilitation_score' not in st.session_state:
        st.session_state.design_facilitation_score = 0
    if 'voice_score' not in st.session_state:
        st.session_state.voice_score = 0
    if 'reciprocity_score' not in st.session_state:
        st.session_state.reciprocity_score = 0
    if 'civic_learning_score' not in st.session_state:
        st.session_state.civic_learning_score = 0
    if 'critical_reflection_score' not in st.session_state:
        st.session_state.critical_reflection_score = 0
    if 'integration_score' not in st.session_state:
        st.session_state.integration_score = 0
    if 'goals_met_score' not in st.session_state:
        st.session_state.goals_met_score = 0
    if 'outputs_delivered_score' not in st.session_state:
        st.session_state.outputs_delivered_score = 0
    if 'capacities_capabilities_score' not in st.session_state:
        st.session_state.capacities_capabilities_score = 0
    if 'sustainability_score' not in st.session_state:
        st.session_state.sustainability_score = 0
    if 'response_id' not in st.session_state:
        st.session_state.response_id = ''
    if 'first_degree' not in st.session_state:
        st.session_state.first_degree = {}
    if 'second_degree' not in st.session_state:
        st.session_state.second_degree = {}
    if 'third_degree' not in st.session_state:
        st.session_state.third_degree = {}

def initiate_survey():
    initialize_session_state()
    st.title("Project Alignment Survey")

    if st.session_state.page == 0:
        ask_for_unique_id()
    elif st.session_state.page == 1:
        page_1()
    elif st.session_state.page == 2:
        page_2()
    elif st.session_state.page == 3:
        page_3()
    elif st.session_state.page == 4:
        page_4()
    elif st.session_state.page == 5:
        page_5()

def ask_for_unique_id():
    st.header("Enter your projectID to continue")
    unique_id = st.text_input("projectID")

    if st.button("Continue"):
        if unique_id:
            with driver.session() as session:
                try:
                    exists = session.execute_read(check_unique_id, unique_id)
                    if exists:
                        st.session_state.projectID = unique_id
                        st.session_state.page = 1
                        st.rerun()
                    else:
                        st.error("Invalid Unique ID. Please check your ID or initiate a new survey.")
                except Exception as e:
                    st.error(f"An error occurred while checking the unique ID: {e}")
        else:
            st.error("Please enter a unique ID to continue")

def page_1():
    st.title("Project Alignment Survey - Page 1")

    with st.form("page_1"):
        st.session_state.project_name = st.text_input("Project Name")
        
        st.subheader("Connection to the Project")
        st.session_state.connection = st.selectbox("How are you connected to the project?", ["Research Team", "Community", "Institutional Partner"])

        st.subheader("The research team and the partners were aligned in terms of:")
        st.session_state.alignment_goals = st.slider("The Goals and Purposes of the project", 0.0, 1.0, 0.5)
        st.session_state.alignment_values = st.slider("The Values and Ideals that guide the project", 0.0, 1.0, 0.5)
        st.session_state.alignment_roles = st.slider("Setting the Roles and Responsibilities between the research team and the community partners", 0.0, 1.0, 0.5)
        st.session_state.alignment_resources = st.slider("Managing the Resources that move the project forward", 0.0, 1.0, 0.5)
        st.session_state.alignment_activities = st.slider("Designing and Facilitating the Activities and Events for the good of the community in the project", 0.0, 1.0, 0.5)
        st.session_state.alignment_culture = st.slider("Empowering the Culture, Knowledge and Language of the community in the work of the project", 0.0, 1.0, 0.5)
        st.session_state.alignment_outputs = st.slider("The types of Outputs such as workshops and events, news stories, policy documents, and academic articles and presentations", 0.0, 1.0, 0.5)
        st.session_state.alignment_outcomes = st.slider("The Outcomes of the project in terms of short-term and long-term changes", 0.0, 1.0, 0.5)

        next_page = st.form_submit_button("Next")

    if next_page:
        st.session_state.page = 2
        st.rerun()

def page_2():
    st.title("Project Alignment Survey - Page 2")

    # Initialize all required session state variables
    st.header("Please select the scores you would like to include in your report.")
    st.session_state.selected_scores = st.multiselect("Select Scores", ["Direct Indicator Scores", "Project Impact Scores", "Alignment Scores", "Ripple Effect Scores"], default=st.session_state.get('selected_scores', []))

    multipliers = [
        (1, "(1)"),
        (0.95, "(0.95)"),
        (0.90, "(0.90)"),
        (0.84, "(0.84)"),
        (0.78, "(0.78)")
    ]

    # Define the questions and their weights
    st.subheader("Challenge Origin")
    challenge_origin_items = [
        "The Research Team identified the challenge or issue (0.78)",
        "The Community identified the challenge or issue (0.95)",
        "There were ongoing negotiations between the Research Team and the Community (1)",
        "The Research Team refined the challenge or issue (0.84)",
        "The Community refined the challenge or issue (0.90)"
    ]
    st.session_state.challenge_origin = sort_items([
        {'header': 'Does Not Describe My Project', 'items': challenge_origin_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.challenge_origin_score = calculate_sortable_score(st.session_state.challenge_origin[1]['items'], multipliers)

    st.subheader("Diversity")
    diversity_items = [
        "The Research Team is diverse in multiple ways and represents a range of identities (0.78)",
        "The Community is diverse in multiple ways and represents a range of identities (0.84)",
        "Underrepresented and/or marginalized identities are a part of the Research Team (0.90)",
        "Underrepresented and/or marginalized identities are a part of the Community (0.95)",
        "There are overlaps in identity memberships between the Research Team and the Community (1)"
    ]
    st.session_state.diversity = sort_items([
        {'header': 'Does Not Describe My Project', 'items': diversity_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.diversity_score = calculate_sortable_score(st.session_state.diversity[1]['items'], multipliers)

    st.subheader("Resources")
    resources_items = [
        "All resources were provided by the Research Team (0.84)",
        "The Research Team contributed resources (0.90)",
        "There were ongoing negotiations between the Research Team and the Community about the commitment of resources (1)",
        "The Community contributed resources (0.95)",
        "All resources were provided by the Community (0.78)"
    ]
    st.session_state.resources = sort_items([
        {'header': 'Does Not Describe My Project', 'items': resources_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.resources_score = calculate_sortable_score(st.session_state.resources[1]['items'], multipliers)

    st.subheader("Trust")
    trust_items = [
        "Despite a history of mistrust, the Research Team reached out to the Community (0.90)",
        "Building on a history of trust and collaboration, the Research Team reached out to the Community (0.78)",
        "There were ongoing trust-building efforts between the Research Institution and the Community (1)",
        "Building on a history of trust and collaboration, the Community reached out to the Research Team (0.84)",
        "Despite a history of mistrust, the Community reached out to the Research Team (0.95)"
    ]
    st.session_state.trust = sort_items([
        {'header': 'Does Not Describe My Project', 'items': trust_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.trust_score = calculate_sortable_score(st.session_state.trust[1]['items'], multipliers)

    st.subheader("Beneficence")
    beneficence_items = [
        "The Research Team benefitted from the processes (0.78)",
        "The Community Partners benefitted from the processes (0.90)",
        "There were ongoing discussions to ensure both the Community and the Research Team would benefit (1)",
        "Benefits built upon and strengthened the Community’s cultural capital and wealth and agency (0.95)",
        "Benefits aligned with the goals and purposes of the project (0.84)"
    ]
    st.session_state.beneficence = sort_items([
        {'header': 'Does Not Describe My Project', 'items': beneficence_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.beneficence_score = calculate_sortable_score(st.session_state.beneficence[1]['items'], multipliers)

    st.subheader("Reflection")
    reflection_items = [
        "The Research Team engaged in and benefitted from intentional reflection activities (0.78)",
        "Community partners engaged in and benefitted from intentional reflection activities (0.84)",
        "The Research Team and Community partners engaged in and benefitted from intentional collaborative reflection activities (1)",
        "Lessons learned for all participants were identified through intentional reflection activities (0.90)",
        "Strategies and new practices were developed through intentional reflection activities (0.95)"
    ]
    st.session_state.reflection = sort_items([
        {'header': 'Does Not Describe My Project', 'items': reflection_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.reflection_score = calculate_sortable_score(st.session_state.reflection[1]['items'], multipliers)

    st.subheader("Decision Making")
    decision_making_items = [
        "The Research Team contributed to the decision making processes (0.78)",
        "Community Partners contributed to the decision making processes (0.84)",
        "Decision making was conducted through clear and understood processes (1)",
        "Decision making processes recognized and supported the community’s cultural capital and agency (0.95)",
        "Decisions were made to align with the goals and purposes of the project (0.90)"
    ]
    st.session_state.decision_making = sort_items([
        {'header': 'Does Not Describe My Project', 'items': decision_making_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.decision_making_score = calculate_sortable_score(st.session_state.decision_making[1]['items'], multipliers)

    st.subheader("Tool Construction")
    tool_construction_items = [
        "Promoted Efficiency (0.84)",
        "The Research Team contributed to building the tools (0.78)",
        "Recognized and supported the Community’s cultural wealth and capital and agency (1)",
        "Made processes more clear and understandable (0.95)",
        "The Community contributed to building the tools (0.90)"
    ]
    st.session_state.tool_construction = sort_items([
        {'header': 'Does Not Describe My Project', 'items': tool_construction_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.tool_construction_score = calculate_sortable_score(st.session_state.tool_construction[1]['items'], multipliers)

    if st.button("Next"):
        st.session_state.page = 3
        st.rerun()
    
    if st.button("Previous"):
        st.session_state.page = 1
        st.rerun()

def page_3():
    st.title("Project Alignment Survey - Page 3")

    multipliers = [
        (1, "(1)"),
        (0.95, "(0.95)"),
        (0.90, "(0.90)"),
        (0.84, "(0.84)"),
        (0.78, "(0.78)")
    ]

    st.subheader("Duration")
    duration_items = [
        "A Week or Less (0.78)",
        "A Month or Less (0.84)",
        "A Semester or Less (0.90)",
        "A Year or Less (0.95)",
        "Multiple Years (1)"
    ]
    st.session_state.duration = sort_items([
        {'header': 'Does Not Describe My Project', 'items': duration_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.duration_score = calculate_sortable_score(st.session_state.duration[1]['items'], multipliers)

    st.subheader("Frequency")
    frequency_items = [
        "Once (0.78)",
        "More than once (0.84)",
        "At least Monthly (0.90)",
        "At least Weekly (0.95)",
        "Daily or more (1)"
    ]
    st.session_state.frequency = sort_items([
        {'header': 'Does Not Describe My Project', 'items': frequency_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.frequency_score = calculate_sortable_score(st.session_state.frequency[1]['items'], multipliers)

    st.subheader("Research Questions")
    research_questions_items = [
        "The Research Team contributed to the research question or questions to be explored (0.78)",
        "The Community contributed to the research question or questions to be explored (0.95)",
        "The research question or questions recognized and supported the Community’s cultural wealth and capital and agency (0.90)",
        "The research question or questions were designed to align with the goals and purposes of the project (0.84)",
        "The research question or questions provided opportunities to generate new understandings for the discipline(s) of the Research Team and to benefit the Community (1)"
    ]
    st.session_state.research_questions = sort_items([
        {'header': 'Does Not Describe My Project', 'items': research_questions_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.research_questions_score = calculate_sortable_score(st.session_state.research_questions[1]['items'], multipliers)

    st.subheader("Design and Facilitation")
    design_facilitation_items = [
        "The Research Team contributed to the design and facilitation of interventions and research (0.78)",
        "The Community contributed to the design and facilitation of interventions and research (0.95)",
        "The design and facilitation of interventions and research recognized and supported the Community’s cultural wealth and capital and agency (0.90)",
        "The design and facilitation of interventions and research aligned with the goals and purposes of the project (0.84)",
        "The design and facilitation of interventions and research provided opportunities to generate new understandings for the discipline(s) and to benefit the Community (1)"
    ]
    st.session_state.design_facilitation = sort_items([
        {'header': 'Does Not Describe My Project', 'items': design_facilitation_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.design_facilitation_score = calculate_sortable_score(st.session_state.design_facilitation[1]['items'], multipliers)

    st.subheader("Voice")
    voice_items = [
        "Materials and Events utilized Academic Language (0.78)",
        "Materials and Events utilized Community-Centered Language (0.90)",
        "Materials and Events were aligned with the goals and purposes of the project (0.84)",
        "Materials and Events were fit specifically for local settings (0.95)",
        "Materials and Events were culture-centered activities (1)"
    ]
    st.session_state.voice = sort_items([
        {'header': 'Does Not Describe My Project', 'items': voice_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.voice_score = calculate_sortable_score(st.session_state.voice[1]['items'], multipliers)

    st.subheader("Reciprocity")
    reciprocity_items = [
        "Expectations around Community benefit and Student learning are included in the course syllabus (0.78)",
        "Student accountability to the Community and Community benefit are shared with Students (0.84)",
        "The Instructor facilitates an activity or activities that benefit the Community and enrich Student learning (0.9)",
        "Activities are co-constructed by the Instructor, Community, and Students that benefit the Community and enrich Student learning (0.95)",
        "There is ongoing collaboration between the Community, the Instructor, and Students in all phases of the project or engaged experience (1)"
    ]
    st.session_state.reciprocity = sort_items([
        {'header': 'Does Not Describe My Project', 'items': reciprocity_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.reciprocity_score = calculate_sortable_score(st.session_state.reciprocity[1]['items'], multipliers)

    st.subheader("Civic Learning")
    civic_learning_items = [
        "Civic learning expectations and outcomes are included in the course syllabus (0.78)",
        "There is an alignment across the syllabus, the activities, and the assessments to ensure civic learning is a measured component of the course (0.9)",
        "Course and community activities are facilitated to support civic learning (0.84)",
        "Opportunities are offered for meaning-making and making connections between civic learning and academic work in the course (0.95)",
        "Opportunities are offered for meaning-making and making connections between civic learning and real-world contexts (1)"
    ]
    st.session_state.civic_learning = sort_items([
        {'header': 'Does Not Describe My Project', 'items': civic_learning_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.civic_learning_score = calculate_sortable_score(st.session_state.civic_learning[1]['items'], multipliers)

    st.subheader("Critical Reflection")
    critical_reflection_items = [
        "Expectations for critical reflection is built into the course requirements and are stated in the syllabus (0.78)",
        "There are ongoing critical reflection activities with scaffolding that allow deepened reflections on engaged experiences (0.84)",
        "Critical reflection activities are offered that help students make connections across course content and beyond (1)",
        "Critical reflection activities are used to enhance course content (0.95)",
        "Critical reflection activities are used to deepen collaborative relationships with the Community (1)"
    ]
    st.session_state.critical_reflection = sort_items([
        {'header': 'Does Not Describe My Project', 'items': critical_reflection_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.critical_reflection_score = calculate_sortable_score(st.session_state.critical_reflection[1]['items'], multipliers)

    st.subheader("Integration")
    integration_items = [
        "Relationships and dynamics between the Instructor, the Community, and the Students are similar to the relationships and dynamics of the broader research project (0.84)",
        "The Community is included in the decision making around the inclusion of engaged learning in the broader research project (0.9)",
        "Students’ engagement activities with the Community support research and intervention activities by building capacities and capabilities and/or generating useful understandings and/or practices (0.95)",
        "Course artifacts and outputs support research and intervention activities by building capacities and capabilities and/or generating useful understandings and/or practices (1)"
    ]
    st.session_state.integration = sort_items([
        {'header': 'Does Not Describe My Project', 'items': integration_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.integration_score = calculate_sortable_score(st.session_state.integration[1]['items'], multipliers)

    st.subheader("Goals Met")
    goals_met_items = [
        "Entirely for the Research Team (1)",
        "Mostly for the Research Team, some for the Community (0.95)",
        "Equally for the Research Team and the Community (0.90)",
        "Mostly for the Community, some for the Research Team (0.84)",
        "Entirely for the Community (0.78)"
    ]
    st.session_state.goals_met = sort_items([
        {'header': 'Does Not Describe My Project', 'items': goals_met_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.goals_met_score = calculate_sortable_score(st.session_state.goals_met[1]['items'], multipliers)

    st.subheader("Outputs Delivered")
    outputs_delivered_items = [
        "Academic Outputs that Benefit the Research Team (0.78)",
        "Academic Outputs that Advance the Field (0.84)",
        "Community-Based Outputs that Benefit Direct Community Partners (0.90)",
        "Community-Based Outputs that Reach Broader Community Members and Institutions (1)",
        "Academic and/or Community-Based Outputs in a Range of Venues (0.95)"
    ]
    st.session_state.outputs_delivered = sort_items([
        {'header': 'Does Not Describe My Project', 'items': outputs_delivered_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.outputs_delivered_score = calculate_sortable_score(st.session_state.outputs_delivered[1]['items'], multipliers)

    st.subheader("Capacities and Capabilities Strengthened")
    capacities_capabilities_items = [
        "Participant and/or Community well-being (0.90)",
        "Participant and/or Community agency (1)",
        "Mutual trust and respect between the Community and the Research Team and/or the Research Institution (0.78)",
        "The distribution of opportunity and/or attainment (0.84)",
        "The fabric and cohesion of the Community (0.95)"
    ]
    st.session_state.capacities_capabilities = sort_items([
        {'header': 'Does Not Describe My Project', 'items': capacities_capabilities_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.capacities_capabilities_score = calculate_sortable_score(st.session_state.capacities_capabilities[1]['items'], multipliers)

    st.subheader("Sustainability")
    sustainability_items = [
        "Trust and respect in partnership (0.84)",
        "Available resources (0.78)",
        "Ongoing shared vision and common goals (1)",
        "Concrete strategies for further engagement (0.90)",
        "Infrastructures for further engagement (0.95)"
    ]
    st.session_state.sustainability = sort_items([
        {'header': 'Does Not Describe My Project', 'items': sustainability_items},
        {'header': 'Describes My Project', 'items': []}
    ], multi_containers=True, direction="vertical")
    st.session_state.sustainability_score = calculate_sortable_score(st.session_state.sustainability[1]['items'], multipliers)
    
    s1 = st.session_state.challenge_origin_score + st.session_state.diversity_score + st.session_state.trust_score + st.session_state.resources_score
    s2 = st.session_state.beneficence_score + st.session_state.reflection_score + st.session_state.decision_making_score + st.session_state.tool_construction_score
    s3 = st.session_state.duration_score + st.session_state.frequency_score + st.session_state.research_questions_score + st.session_state.design_facilitation_score
    s4 = st.session_state.reciprocity_score + st.session_state.civic_learning_score + st.session_state.critical_reflection_score + st.session_state.integration_score
    s5 = st.session_state.goals_met_score + st.session_state.outputs_delivered_score + st.session_state.capacities_capabilities_score + st.session_state.sustainability_score
    
    st.session_state.context_score = s1
    st.session_state.processes_score = s2
    st.session_state.interventions_and_research_score = s3
    st.session_state.engaged_learners_score = s4
    st.session_state.outcomes_score = s5 
    
    
    #DEBUG SCORES
    # st.write("context score: ", st.session_state.context_score)  
    # st.write("processes score: ", st.session_state.processes_score)
    # st.write("interventions and research score: ", st.session_state.interventions_and_research_score)
    # st.write("engaged learners score: ", st.session_state.engaged_learners_score)
    # st.write("outcomes score: ", st.session_state.outcomes_score)
    
    
    if st.button("Next"):
        st.session_state.page = 4
        st.rerun()

    if st.button("Previous"):
        st.session_state.page = 2
        st.rerun()

def page_4():
    st.title("Project Alignment Survey")

    st.subheader("FIRST DEGREE")
    st.session_state.first_degree['number_of_research_team_members'] = st.number_input("How many Faculty Members were a part of the Research Team?")
    st.session_state.first_degree['number_of_staff_members'] = st.number_input("How many Staff Members were a part of the Research Team?")
    st.session_state.first_degree['number_of_student_assistants'] = st.number_input("How many Student Assistants (research assistants, etc.) were a part of the Research Team?")
    st.session_state.first_degree['number_of_students'] = st.number_input("How many Students (service learning, etc.) contributed to the project?")
    st.session_state.first_degree['number_of_core_community_members'] = st.number_input("How many individual Core Community Members contributed to the Project?")
    st.session_state.first_degree['community_institution_contribution'] = st.number_input("Number Representatives of Community Institutions contributed to the Project")

    st.subheader("SECOND DEGREE")
    st.write("Please answer the following realistically.")
    st.session_state.second_degree['faculty_influence'] = st.number_input("How many people can Faculty Members influence based on their transformation by participating in the project?")
    st.session_state.second_degree['staff_influence'] = st.number_input("How many people can Staff Members influence based on their transformation by participating in the project?")
    st.session_state.second_degree['student_assistants_influence'] = st.number_input("How many people can Student Assistants influence based on their transformation by participating in the project?")
    st.session_state.second_degree['students_influence'] = st.number_input("How many people can Students influence based on their transformation by participating in the project?")
    st.session_state.second_degree['core_community_members_influence'] = st.number_input("How many people can Core Community Members influence based on their transformation by participating in the project?")
    st.session_state.second_degree['community_institution_influence'] = st.number_input("How many people can Representatives of Community Institutions influence based on their transformation by participating in the project?")
    st.session_state.second_degree['within_group_likelihood'] = st.slider("How likely is it that any member within a group influenced by the same person will be connected to someone else within the same group?", 0.0, 0.90, 0.5)
    st.session_state.second_degree['outside_group_likelihood'] = st.slider("How likely is it that any member of any group will be connected to someone outside their group?", 0.0, 0.90, 0.5)

    if st.button("Next"):
        st.session_state.page = 5
        st.rerun()

    if st.button("Previous"):
        st.session_state.page = 3
        st.rerun()

def page_5():
    st.title("Project Alignment Survey - Third Degree")

    st.write("Please answer the following realistically.")
    st.session_state.third_degree['faculty_further_influence'] = st.number_input("How many people can those influenced by Faculty Members further influence?")
    st.session_state.third_degree['staff_further_influence'] = st.number_input("How many people can those influenced by Staff Members further influence?")
    st.session_state.third_degree['student_assistants_further_influence'] = st.number_input("How many people can those influenced by Student Assistants further influence?")
    st.session_state.third_degree['students_further_influence'] = st.number_input("How many people can Students influence based on their transformation by participating in the project?")
    st.session_state.third_degree['core_community_members_further_influence'] = st.number_input("How many people can those influenced by Core Community Members further influence?")
    st.session_state.third_degree['community_institution_further_influence'] = st.number_input("How many people can those influenced by Representatives of Community Institutions further influence?")
    st.session_state.third_degree['within_group_likelihood'] = st.slider("How likely is it that any member within a group influenced by the same person will be connected to someone else within the same group?", 0.0, 0.90, 0.5)
    st.session_state.third_degree['outside_group_likelihood'] = st.slider("How likely is it that any member of any group will be connected to someone outside their group?", 0.0, 0.90, 0.5)
    
    
    st.write("Your Unique response ID:", st.session_state.response_id)
    st.warning("Please save this ID for future reference.")

    if st.button("Submit"):
        submit_survey()
    
    if st.button("Previous"):
        st.session_state.page = 4
        st.rerun()

def submit_survey():
    if 'response_id' not in st.session_state or not st.session_state.response_id:
        st.session_state.response_id = generate_unique_id(12)

    preferences = {
        "unique_id": st.session_state.projectID,
        "project_name": st.session_state.project_name,
        "partners": json.dumps(st.session_state.partners),  # Ensure partners is a JSON string
        "score_visualizations": json.dumps(st.session_state.selected_scores),  # Ensure score_visualizations is a JSON string
        "direct_indicator_preferences": json.dumps(st.session_state.direct_indicator_preferences),  # Convert to JSON string
        "challenge_origin_score": st.session_state.challenge_origin_score,
        "diversity_score": st.session_state.diversity_score,
        "resources_score": st.session_state.resources_score,
        "beneficence_score": st.session_state.beneficence_score,
        "reflection_score": st.session_state.reflection_score,
        "decision_making_score": st.session_state.decision_making_score,
        "tool_construction_score": st.session_state.tool_construction_score,
        "trust_score": st.session_state.trust_score,
        "duration_score": st.session_state.duration_score,
        "frequency_score": st.session_state.frequency_score,
        "research_questions_score": st.session_state.research_questions_score,
        "design_facilitation_score": st.session_state.design_facilitation_score,
        "voice_score": st.session_state.voice_score,
        "reciprocity_score": st.session_state.reciprocity_score,
        "civic_learning_score": st.session_state.civic_learning_score,
        "critical_reflection_score": st.session_state.critical_reflection_score,
        "integration_score": st.session_state.integration_score,
        "goals_met_score": st.session_state.goals_met_score,
        "outputs_delivered_score": st.session_state.outputs_delivered_score,
        "capacities_capabilities_score": st.session_state.capacities_capabilities_score,
        "sustainability_score": st.session_state.sustainability_score,
        "projectID": st.session_state.projectID,  # Ensure projectID is included
        "context_score": st.session_state.context_score,
        "processes_score": st.session_state.processes_score,
        "interventions_and_research_score": st.session_state.interventions_and_research_score,
        "engaged_learners_score": st.session_state.engaged_learners_score,
        "outcomes_score": st.session_state.outcomes_score,
        "response_id": st.session_state.response_id,  # Add response ID
        "connection": st.session_state.connection,
        "alignment_goals": st.session_state.alignment_goals,
        "alignment_values": st.session_state.alignment_values,
        "alignment_roles": st.session_state.alignment_roles,
        "alignment_resources": st.session_state.alignment_resources,
        "alignment_activities": st.session_state.alignment_activities,
        "alignment_culture": st.session_state.alignment_culture,
        "alignment_outputs": st.session_state.alignment_outputs,
        "alignment_outcomes": st.session_state.alignment_outcomes,
        "first_degree": json.dumps(st.session_state.first_degree),
        "second_degree": json.dumps(st.session_state.second_degree),
        "third_degree": json.dumps(st.session_state.third_degree)
    }

    # Print types for debugging
    for key, value in preferences.items():
        print(f"{key} ({type(value)}): {value}")

    with driver.session() as session:
        session.execute_write(create_survey_in_db, preferences)

    st.success("Survey Saved Successfully!")

def create_survey_in_db(tx, preferences):
    query = """
    CREATE (s:Survey {response_id: $response_id, projectID: $projectID})
    MERGE (project:Project {unique_id: $unique_id})
    SET project.project_name = $project_name, 
        project.projectID = $projectID,
        project.partners = $partners,
        project.score_visualizations = $score_visualizations,
        project.direct_indicator_preferences = $direct_indicator_preferences,
        project.challenge_origin_score = $challenge_origin_score,
        project.diversity_score = $diversity_score,
        project.resources_score = $resources_score,
        project.beneficence_score = $beneficence_score,
        project.reflection_score = $reflection_score,
        project.decision_making_score = $decision_making_score,
        project.tool_construction_score = $tool_construction_score,
        project.trust_score = $trust_score,
        project.duration_score = $duration_score,
        project.frequency_score = $frequency_score,
        project.research_questions_score = $research_questions_score,
        project.design_facilitation_score = $design_facilitation_score,
        project.voice_score = $voice_score,
        project.reciprocity_score = $reciprocity_score,
        project.civic_learning_score = $civic_learning_score,
        project.critical_reflection_score = $critical_reflection_score,
        project.integration_score = $integration_score,
        project.goals_met_score = $goals_met_score,
        project.outputs_delivered_score = $outputs_delivered_score,
        project.capacities_capabilities_score = $capacities_capabilities_score,
        project.sustainability_score = $sustainability_score,
        project.context_score = $context_score,
        project.processes_score = $processes_score,
        project.interventions_and_research_score = $interventions_and_research_score,
        project.engaged_learners_score = $engaged_learners_score,
        project.outcomes_score = $outcomes_score
    SET s.connection = $connection,
        s.alignment_goals = $alignment_goals,
        s.alignment_values = $alignment_values,
        s.alignment_roles = $alignment_roles,
        s.alignment_resources = $alignment_resources,
        s.alignment_activities = $alignment_activities,
        s.alignment_culture = $alignment_culture,
        s.alignment_outputs = $alignment_outputs,
        s.alignment_outcomes = $alignment_outcomes,
        s.context_score = $context_score,
        s.processes_score = $processes_score,
        s.interventions_and_research_score = $interventions_and_research_score,
        s.engaged_learners_score = $engaged_learners_score,
        s.outcomes_score = $outcomes_score,
        s.first_degree = $first_degree,
        s.second_degree = $second_degree,
        s.third_degree = $third_degree
    """
    tx.run(query, **preferences)

if __name__ == "__main__":
    initiate_survey()




# import os
# from dotenv import load_dotenv
# from neo4j import GraphDatabase
# import streamlit as st
# from utils.unique_id import generate_unique_id
# from opencage.geocoder import OpenCageGeocode
# from opencage.geocoder import RateLimitExceededError
# from streamlit_sortables import sort_items
# import json
# from scipy.stats import gmean

# # Load environment variables from .env file
# load_dotenv()

# # Get the values from environment variables
# api_key = os.getenv('OPEN_CAGE_API_KEY')
# uri = os.getenv('NEO4J_URI')
# user = os.getenv('NEO4J_USER')
# password = os.getenv('NEO4J_PASSWORD')

# geocoder = OpenCageGeocode(api_key)
# driver = GraphDatabase.driver(uri, auth=(user, password))

# multipliers = [
#     (1, "(1)"),
#     (0.95, "(0.95)"),
#     (0.90, "(0.90)"),
#     (0.84, "(0.84)"),
#     (0.78, "(0.78)")
# ]

# def check_unique_id(tx, projectID):
#     query = "MATCH (project:Project {projectID: $projectID}) RETURN project"
#     result = tx.run(query, projectID=projectID)
#     return result.single() is not None

# def calculate_sortable_score(items, multipliers):
#     score = 0
#     for i, item in enumerate(items):
#         for weight, text in multipliers:
#             if text in item:
#                 score += weight * (1 - 0.05 * i)
#     return score / 4.027

# def initialize_session_state():
#     if 'page' not in st.session_state:
#         st.session_state.page = 0
#     if 'projectID' not in st.session_state:
#         st.session_state.projectID = ''
#     if 'project_name' not in st.session_state:
#         st.session_state.project_name = ''
#     if 'partners' not in st.session_state:
#         st.session_state.partners = []
#     if 'selected_scores' not in st.session_state:
#         st.session_state.selected_scores = []
#     if 'direct_indicator_preferences' not in st.session_state:
#         st.session_state.direct_indicator_preferences = {}
#     if 'challenge_origin_score' not in st.session_state:
#         st.session_state.challenge_origin_score = 0
#     if 'diversity_score' not in st.session_state:
#         st.session_state.diversity_score = 0
#     if 'resources_score' not in st.session_state:
#         st.session_state.resources_score = 0
#     if 'beneficence_score' not in st.session_state:
#         st.session_state.beneficence_score = 0
#     if 'reflection_score' not in st.session_state:
#         st.session_state.reflection_score = 0
#     if 'decision_making_score' not in st.session_state:
#         st.session_state.decision_making_score = 0
#     if 'tool_construction_score' not in st.session_state:
#         st.session_state.tool_construction_score = 0
#     if 'trust_score' not in st.session_state:
#         st.session_state.trust_score = 0
#     if 'duration_score' not in st.session_state:
#         st.session_state.duration_score = 0
#     if 'frequency_score' not in st.session_state:
#         st.session_state.frequency_score = 0
#     if 'research_questions_score' not in st.session_state:
#         st.session_state.research_questions_score = 0
#     if 'design_facilitation_score' not in st.session_state:
#         st.session_state.design_facilitation_score = 0
#     if 'voice_score' not in st.session_state:
#         st.session_state.voice_score = 0
#     if 'reciprocity_score' not in st.session_state:
#         st.session_state.reciprocity_score = 0
#     if 'civic_learning_score' not in st.session_state:
#         st.session_state.civic_learning_score = 0
#     if 'critical_reflection_score' not in st.session_state:
#         st.session_state.critical_reflection_score = 0
#     if 'integration_score' not in st.session_state:
#         st.session_state.integration_score = 0
#     if 'goals_met_score' not in st.session_state:
#         st.session_state.goals_met_score = 0
#     if 'outputs_delivered_score' not in st.session_state:
#         st.session_state.outputs_delivered_score = 0
#     if 'capacities_capabilities_score' not in st.session_state:
#         st.session_state.capacities_capabilities_score = 0
#     if 'sustainability_score' not in st.session_state:
#         st.session_state.sustainability_score = 0
#     if 'response_id' not in st.session_state:
#         st.session_state.response_id = ''

# def initiate_survey():
#     initialize_session_state()
#     st.title("Project Alignment Survey")

#     if st.session_state.page == 0:
#         ask_for_unique_id()
#     elif st.session_state.page == 1:
#         page_1()
#     elif st.session_state.page == 2:
#         page_2()
#     elif st.session_state.page == 3:
#         page_3()

# def ask_for_unique_id():
#     st.header("Enter your projectID to continue")
#     unique_id = st.text_input("projectID")

#     if st.button("Continue"):
#         if unique_id:
#             with driver.session() as session:
#                 try:
#                     exists = session.execute_read(check_unique_id, unique_id)
#                     if exists:
#                         st.session_state.projectID = unique_id
#                         st.session_state.page = 1
#                         st.rerun()
#                     else:
#                         st.error("Invalid Unique ID. Please check your ID or initiate a new survey.")
#                 except Exception as e:
#                     st.error(f"An error occurred while checking the unique ID: {e}")
#         else:
#             st.error("Please enter a unique ID to continue")

# def page_1():
#     st.title("Project Alignment Survey - Page 1")

#     with st.form("page_1"):
#         st.session_state.project_name = st.text_input("Project Name")
        
#         st.subheader("Connection to the Project")
#         st.session_state.connection = st.selectbox("How are you connected to the project?", ["Research Team", "Community", "Institutional Partner"])

#         st.subheader("The research team and the partners were aligned in terms of:")
#         st.session_state.alignment_goals = st.slider("The Goals and Purposes of the project", 0.0, 1.0, 0.5)
#         st.session_state.alignment_values = st.slider("The Values and Ideals that guide the project", 0.0, 1.0, 0.5)
#         st.session_state.alignment_roles = st.slider("Setting the Roles and Responsibilities between the research team and the community partners", 0.0, 1.0, 0.5)
#         st.session_state.alignment_resources = st.slider("Managing the Resources that move the project forward", 0.0, 1.0, 0.5)
#         st.session_state.alignment_activities = st.slider("Designing and Facilitating the Activities and Events for the good of the community in the project", 0.0, 1.0, 0.5)
#         st.session_state.alignment_culture = st.slider("Empowering the Culture, Knowledge and Language of the community in the work of the project", 0.0, 1.0, 0.5)
#         st.session_state.alignment_outputs = st.slider("The types of Outputs such as workshops and events, news stories, policy documents, and academic articles and presentations", 0.0, 1.0, 0.5)
#         st.session_state.alignment_outcomes = st.slider("The Outcomes of the project in terms of short-term and long-term changes", 0.0, 1.0, 0.5)

#         next_page = st.form_submit_button("Next")

#     if next_page:
#         st.session_state.page = 2
#         st.rerun()

# def page_2():
#     st.title("Project Alignment Survey - Page 2")

#     # Initialize all required session state variables
#     st.header("Please select the scores you would like to include in your report.")
#     st.session_state.selected_scores = st.multiselect("Select Scores", ["Direct Indicator Scores", "Project Impact Scores", "Alignment Scores", "Ripple Effect Scores"], default=st.session_state.get('selected_scores', []))

#     multipliers = [
#         (1, "(1)"),
#         (0.95, "(0.95)"),
#         (0.90, "(0.90)"),
#         (0.84, "(0.84)"),
#         (0.78, "(0.78)")
#     ]

#     # Define the questions and their weights
#     st.subheader("Challenge Origin")
#     challenge_origin_items = [
#         "The Research Team identified the challenge or issue (0.78)",
#         "The Community identified the challenge or issue (0.95)",
#         "There were ongoing negotiations between the Research Team and the Community (1)",
#         "The Research Team refined the challenge or issue (0.84)",
#         "The Community refined the challenge or issue (0.90)"
#     ]
#     st.session_state.challenge_origin = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': challenge_origin_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.challenge_origin_score = calculate_sortable_score(st.session_state.challenge_origin[1]['items'], multipliers)

#     st.subheader("Diversity")
#     diversity_items = [
#         "The Research Team is diverse in multiple ways and represents a range of identities (0.78)",
#         "The Community is diverse in multiple ways and represents a range of identities (0.84)",
#         "Underrepresented and/or marginalized identities are a part of the Research Team (0.90)",
#         "Underrepresented and/or marginalized identities are a part of the Community (0.95)",
#         "There are overlaps in identity memberships between the Research Team and the Community (1)"
#     ]
#     st.session_state.diversity = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': diversity_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.diversity_score = calculate_sortable_score(st.session_state.diversity[1]['items'], multipliers)

#     st.subheader("Resources")
#     resources_items = [
#         "All resources were provided by the Research Team (0.84)",
#         "The Research Team contributed resources (0.90)",
#         "There were ongoing negotiations between the Research Team and the Community about the commitment of resources (1)",
#         "The Community contributed resources (0.95)",
#         "All resources were provided by the Community (0.78)"
#     ]
#     st.session_state.resources = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': resources_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.resources_score = calculate_sortable_score(st.session_state.resources[1]['items'], multipliers)

#     st.subheader("Trust")
#     trust_items = [
#         "Despite a history of mistrust, the Research Team reached out to the Community (0.90)",
#         "Building on a history of trust and collaboration, the Research Team reached out to the Community (0.78)",
#         "There were ongoing trust-building efforts between the Research Institution and the Community (1)",
#         "Building on a history of trust and collaboration, the Community reached out to the Research Team (0.84)",
#         "Despite a history of mistrust, the Community reached out to the Research Team (0.95)"
#     ]
#     st.session_state.trust = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': trust_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.trust_score = calculate_sortable_score(st.session_state.trust[1]['items'], multipliers)

#     st.subheader("Beneficence")
#     beneficence_items = [
#         "The Research Team benefitted from the processes (0.78)",
#         "The Community Partners benefitted from the processes (0.90)",
#         "There were ongoing discussions to ensure both the Community and the Research Team would benefit (1)",
#         "Benefits built upon and strengthened the Community’s cultural capital and wealth and agency (0.95)",
#         "Benefits aligned with the goals and purposes of the project (0.84)"
#     ]
#     st.session_state.beneficence = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': beneficence_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.beneficence_score = calculate_sortable_score(st.session_state.beneficence[1]['items'], multipliers)

#     st.subheader("Reflection")
#     reflection_items = [
#         "The Research Team engaged in and benefitted from intentional reflection activities (0.78)",
#         "Community partners engaged in and benefitted from intentional reflection activities (0.84)",
#         "The Research Team and Community partners engaged in and benefitted from intentional collaborative reflection activities (1)",
#         "Lessons learned for all participants were identified through intentional reflection activities (0.90)",
#         "Strategies and new practices were developed through intentional reflection activities (0.95)"
#     ]
#     st.session_state.reflection = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': reflection_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.reflection_score = calculate_sortable_score(st.session_state.reflection[1]['items'], multipliers)

#     st.subheader("Decision Making")
#     decision_making_items = [
#         "The Research Team contributed to the decision making processes (0.78)",
#         "Community Partners contributed to the decision making processes (0.84)",
#         "Decision making was conducted through clear and understood processes (1)",
#         "Decision making processes recognized and supported the community’s cultural capital and agency (0.95)",
#         "Decisions were made to align with the goals and purposes of the project (0.90)"
#     ]
#     st.session_state.decision_making = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': decision_making_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.decision_making_score = calculate_sortable_score(st.session_state.decision_making[1]['items'], multipliers)

#     st.subheader("Tool Construction")
#     tool_construction_items = [
#         "Promoted Efficiency (0.84)",
#         "The Research Team contributed to building the tools (0.78)",
#         "Recognized and supported the Community’s cultural wealth and capital and agency (1)",
#         "Made processes more clear and understandable (0.95)",
#         "The Community contributed to building the tools (0.90)"
#     ]
#     st.session_state.tool_construction = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': tool_construction_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.tool_construction_score = calculate_sortable_score(st.session_state.tool_construction[1]['items'], multipliers)

#     if st.button("Next"):
#         st.session_state.page = 3
#         st.rerun()
    
#     if st.button("Previous"):
#         st.session_state.page = 1
#         st.rerun()

# def page_3():
#     st.title("Project Alignment Survey - Page 3")

#     multipliers = [
#         (1, "(1)"),
#         (0.95, "(0.95)"),
#         (0.90, "(0.90)"),
#         (0.84, "(0.84)"),
#         (0.78, "(0.78)")
#     ]

#     st.subheader("Duration")
#     duration_items = [
#         "A Week or Less (0.78)",
#         "A Month or Less (0.84)",
#         "A Semester or Less (0.90)",
#         "A Year or Less (0.95)",
#         "Multiple Years (1)"
#     ]
#     st.session_state.duration = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': duration_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.duration_score = calculate_sortable_score(st.session_state.duration[1]['items'], multipliers)

#     st.subheader("Frequency")
#     frequency_items = [
#         "Once (0.78)",
#         "More than once (0.84)",
#         "At least Monthly (0.90)",
#         "At least Weekly (0.95)",
#         "Daily or more (1)"
#     ]
#     st.session_state.frequency = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': frequency_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.frequency_score = calculate_sortable_score(st.session_state.frequency[1]['items'], multipliers)


#     st.subheader("Research Questions")
#     research_questions_items = [
#         "The Research Team contributed to the research question or questions to be explored (0.78)",
#         "The Community contributed to the research question or questions to be explored (0.95)",
#         "The research question or questions recognized and supported the Community’s cultural wealth and capital and agency (0.90)",
#         "The research question or questions were designed to align with the goals and purposes of the project (0.84)",
#         "The research question or questions provided opportunities to generate new understandings for the discipline(s) of the Research Team and to benefit the Community (1)"
#     ]
#     st.session_state.research_questions = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': research_questions_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.research_questions_score = calculate_sortable_score(st.session_state.research_questions[1]['items'], multipliers)

#     st.subheader("Design and Facilitation")
#     design_facilitation_items = [
#         "The Research Team contributed to the design and facilitation of interventions and research (0.78)",
#         "The Community contributed to the design and facilitation of interventions and research (0.95)",
#         "The design and facilitation of interventions and research recognized and supported the Community’s cultural wealth and capital and agency (0.90)",
#         "The design and facilitation of interventions and research aligned with the goals and purposes of the project (0.84)",
#         "The design and facilitation of interventions and research provided opportunities to generate new understandings for the discipline(s) and to benefit the Community (1)"
#     ]
#     st.session_state.design_facilitation = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': design_facilitation_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.design_facilitation_score = calculate_sortable_score(st.session_state.design_facilitation[1]['items'], multipliers)

#     st.subheader("Voice")
#     voice_items = [
#         "Materials and Events utilized Academic Language (0.78)",
#         "Materials and Events utilized Community-Centered Language (0.90)",
#         "Materials and Events were aligned with the goals and purposes of the project (0.84)",
#         "Materials and Events were fit specifically for local settings (0.95)",
#         "Materials and Events were culture-centered activities (1)"
#     ]
#     st.session_state.voice = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': voice_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.voice_score = calculate_sortable_score(st.session_state.voice[1]['items'], multipliers)

#     st.subheader("Reciprocity")
#     reciprocity_items = [
#         "Expectations around Community benefit and Student learning are included in the course syllabus (0.78)",
#         "Student accountability to the Community and Community benefit are shared with Students (0.84)",
#         "The Instructor facilitates an activity or activities that benefit the Community and enrich Student learning (0.9)",
#         "Activities are co-constructed by the Instructor, Community, and Students that benefit the Community and enrich Student learning (0.95)",
#         "There is ongoing collaboration between the Community, the Instructor, and Students in all phases of the project or engaged experience (1)"
#     ]
#     st.session_state.reciprocity = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': reciprocity_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.reciprocity_score = calculate_sortable_score(st.session_state.reciprocity[1]['items'], multipliers)

#     st.subheader("Civic Learning")
#     civic_learning_items = [
#         "Civic learning expectations and outcomes are included in the course syllabus (0.78)",
#         "There is an alignment across the syllabus, the activities, and the assessments to ensure civic learning is a measured component of the course (0.9)",
#         "Course and community activities are facilitated to support civic learning (0.84)",
#         "Opportunities are offered for meaning-making and making connections between civic learning and academic work in the course (0.95)",
#         "Opportunities are offered for meaning-making and making connections between civic learning and real-world contexts (1)"
#     ]
#     st.session_state.civic_learning = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': civic_learning_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.civic_learning_score = calculate_sortable_score(st.session_state.civic_learning[1]['items'], multipliers)

#     st.subheader("Critical Reflection")
#     critical_reflection_items = [
#         "Expectations for critical reflection is built into the course requirements and are stated in the syllabus (0.78)",
#         "There are ongoing critical reflection activities with scaffolding that allow deepened reflections on engaged experiences (0.84)",
#         "Critical reflection activities are offered that help students make connections across course content and beyond (1)",
#         "Critical reflection activities are used to enhance course content (0.95)",
#         "Critical reflection activities are used to deepen collaborative relationships with the Community (1)"
#     ]
#     st.session_state.critical_reflection = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': critical_reflection_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.critical_reflection_score = calculate_sortable_score(st.session_state.critical_reflection[1]['items'], multipliers)

#     st.subheader("Integration")
#     integration_items = [
#         "Relationships and dynamics between the Instructor, the Community, and the Students are similar to the relationships and dynamics of the broader research project (0.84)",
#         "The Community is included in the decision making around the inclusion of engaged learning in the broader research project (0.9)",
#         "Students’ engagement activities with the Community support research and intervention activities by building capacities and capabilities and/or generating useful understandings and/or practices (0.95)",
#         "Course artifacts and outputs support research and intervention activities by building capacities and capabilities and/or generating useful understandings and/or practices (1)"
#     ]
#     st.session_state.integration = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': integration_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.integration_score = calculate_sortable_score(st.session_state.integration[1]['items'], multipliers)

#     st.subheader("Goals Met")
#     goals_met_items = [
#         "Entirely for the Research Team (1)",
#         "Mostly for the Research Team, some for the Community (0.95)",
#         "Equally for the Research Team and the Community (0.90)",
#         "Mostly for the Community, some for the Research Team (0.84)",
#         "Entirely for the Community (0.78)"
#     ]
#     st.session_state.goals_met = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': goals_met_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.goals_met_score = calculate_sortable_score(st.session_state.goals_met[1]['items'], multipliers)

#     st.subheader("Outputs Delivered")
#     outputs_delivered_items = [
#         "Academic Outputs that Benefit the Research Team (0.78)",
#         "Academic Outputs that Advance the Field (0.84)",
#         "Community-Based Outputs that Benefit Direct Community Partners (0.90)",
#         "Community-Based Outputs that Reach Broader Community Members and Institutions (1)",
#         "Academic and/or Community-Based Outputs in a Range of Venues (0.95)"
#     ]
#     st.session_state.outputs_delivered = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': outputs_delivered_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.outputs_delivered_score = calculate_sortable_score(st.session_state.outputs_delivered[1]['items'], multipliers)

#     st.subheader("Capacities and Capabilities Strengthened")
#     capacities_capabilities_items = [
#         "Participant and/or Community well-being (0.90)",
#         "Participant and/or Community agency (1)",
#         "Mutual trust and respect between the Community and the Research Team and/or the Research Institution (0.78)",
#         "The distribution of opportunity and/or attainment (0.84)",
#         "The fabric and cohesion of the Community (0.95)"
#     ]
#     st.session_state.capacities_capabilities = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': capacities_capabilities_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.capacities_capabilities_score = calculate_sortable_score(st.session_state.capacities_capabilities[1]['items'], multipliers)

#     st.subheader("Sustainability")
#     sustainability_items = [
#         "Trust and respect in partnership (0.84)",
#         "Available resources (0.78)",
#         "Ongoing shared vision and common goals (1)",
#         "Concrete strategies for further engagement (0.90)",
#         "Infrastructures for further engagement (0.95)"
#     ]
#     st.session_state.sustainability = sort_items([
#         {'header': 'Does Not Describe My Project', 'items': sustainability_items},
#         {'header': 'Describes My Project', 'items': []}
#     ], multi_containers=True, direction="vertical")
#     st.session_state.sustainability_score = calculate_sortable_score(st.session_state.sustainability[1]['items'], multipliers)
    
#     s1 = st.session_state.challenge_origin_score + st.session_state.diversity_score + st.session_state.trust_score + st.session_state.resources_score
#     s2 = st.session_state.beneficence_score + st.session_state.reflection_score + st.session_state.decision_making_score + st.session_state.tool_construction_score
#     s3 = st.session_state.duration_score + st.session_state.frequency_score + st.session_state.research_questions_score + st.session_state.design_facilitation_score
#     s4 = st.session_state.reciprocity_score + st.session_state.civic_learning_score + st.session_state.critical_reflection_score + st.session_state.integration_score
#     s5 = st.session_state.goals_met_score + st.session_state.outputs_delivered_score + st.session_state.capacities_capabilities_score + st.session_state.sustainability_score
    
#     st.session_state.context_score = s1
#     st.session_state.processes_score = s2
#     st.session_state.interventions_and_research_score = s3
#     st.session_state.engaged_learners_score = s4
#     st.session_state.outcomes_score = s5 
    
#     st.write("context score: ", st.session_state.context_score)  
#     st.write("processes score: ", st.session_state.processes_score)
#     st.write("interventions and research score: ", st.session_state.interventions_and_research_score)
#     st.write("engaged learners score: ", st.session_state.engaged_learners_score)
#     st.write("outcomes score: ", st.session_state.outcomes_score)
    
#     st.write("Your Unique response ID:", st.session_state.response_id)
#     st.warning("Please save this ID for future reference.")
    
#     if st.button("Submit"):
#         submit_survey()
    
#     if st.button("Previous"):
#         st.session_state.page = 2
#         st.rerun()

# def submit_survey():
#     if 'response_id' not in st.session_state or not st.session_state.response_id:
#         st.session_state.response_id = generate_unique_id(12)

#     preferences = {
#         "unique_id": st.session_state.projectID,
#         "project_name": st.session_state.project_name,
#         "partners": json.dumps(st.session_state.partners),  # Ensure partners is a JSON string
#         "score_visualizations": json.dumps(st.session_state.selected_scores),  # Ensure score_visualizations is a JSON string
#         "direct_indicator_preferences": json.dumps(st.session_state.direct_indicator_preferences),  # Convert to JSON string
#         "challenge_origin_score": st.session_state.challenge_origin_score,
#         "diversity_score": st.session_state.diversity_score,
#         "resources_score": st.session_state.resources_score,
#         "beneficence_score": st.session_state.beneficence_score,
#         "reflection_score": st.session_state.reflection_score,
#         "decision_making_score": st.session_state.decision_making_score,
#         "tool_construction_score": st.session_state.tool_construction_score,
#         "trust_score": st.session_state.trust_score,
#         "duration_score": st.session_state.duration_score,
#         "frequency_score": st.session_state.frequency_score,
#         "research_questions_score": st.session_state.research_questions_score,
#         "design_facilitation_score": st.session_state.design_facilitation_score,
#         "voice_score": st.session_state.voice_score,
#         "reciprocity_score": st.session_state.reciprocity_score,
#         "civic_learning_score": st.session_state.civic_learning_score,
#         "critical_reflection_score": st.session_state.critical_reflection_score,
#         "integration_score": st.session_state.integration_score,
#         "goals_met_score": st.session_state.goals_met_score,
#         "outputs_delivered_score": st.session_state.outputs_delivered_score,
#         "capacities_capabilities_score": st.session_state.capacities_capabilities_score,
#         "sustainability_score": st.session_state.sustainability_score,
#         "projectID": st.session_state.projectID,  # Ensure projectID is included
#         "context_score": st.session_state.context_score,
#         "processes_score": st.session_state.processes_score,
#         "interventions_and_research_score": st.session_state.interventions_and_research_score,
#         "engaged_learners_score": st.session_state.engaged_learners_score,
#         "outcomes_score": st.session_state.outcomes_score,
#         "response_id": st.session_state.response_id,  # Add response ID
#         "connection": st.session_state.connection,
#         "alignment_goals": st.session_state.alignment_goals,
#         "alignment_values": st.session_state.alignment_values,
#         "alignment_roles": st.session_state.alignment_roles,
#         "alignment_resources": st.session_state.alignment_resources,
#         "alignment_activities": st.session_state.alignment_activities,
#         "alignment_culture": st.session_state.alignment_culture,
#         "alignment_outputs": st.session_state.alignment_outputs,
#         "alignment_outcomes": st.session_state.alignment_outcomes
#     }

#     # Print types for debugging
#     for key, value in preferences.items():
#         print(f"{key} ({type(value)}): {value}")

#     with driver.session() as session:
#         session.execute_write(create_survey_in_db, preferences)

#     st.success("Survey Saved Successfully!")

# def create_survey_in_db(tx, preferences):
#     query = """
#     CREATE (s:Survey {response_id: $response_id, projectID: $projectID})
#     MERGE (project:Project {unique_id: $unique_id})
#     SET project.project_name = $project_name, 
#         project.projectID = $projectID,
#         project.partners = $partners,
#         project.score_visualizations = $score_visualizations,
#         project.direct_indicator_preferences = $direct_indicator_preferences,
#         project.challenge_origin_score = $challenge_origin_score,
#         project.diversity_score = $diversity_score,
#         project.resources_score = $resources_score,
#         project.beneficence_score = $beneficence_score,
#         project.reflection_score = $reflection_score,
#         project.decision_making_score = $decision_making_score,
#         project.tool_construction_score = $tool_construction_score,
#         project.trust_score = $trust_score,
#         project.duration_score = $duration_score,
#         project.frequency_score = $frequency_score,
#         project.research_questions_score = $research_questions_score,
#         project.design_facilitation_score = $design_facilitation_score,
#         project.voice_score = $voice_score,
#         project.reciprocity_score = $reciprocity_score,
#         project.civic_learning_score = $civic_learning_score,
#         project.critical_reflection_score = $critical_reflection_score,
#         project.integration_score = $integration_score,
#         project.goals_met_score = $goals_met_score,
#         project.outputs_delivered_score = $outputs_delivered_score,
#         project.capacities_capabilities_score = $capacities_capabilities_score,
#         project.sustainability_score = $sustainability_score,
#         project.context_score = $context_score,
#         project.processes_score = $processes_score,
#         project.interventions_and_research_score = $interventions_and_research_score,
#         project.engaged_learners_score = $engaged_learners_score,
#         project.outcomes_score = $outcomes_score
#     SET s.connection = $connection,
#         s.alignment_goals = $alignment_goals,
#         s.alignment_values = $alignment_values,
#         s.alignment_roles = $alignment_roles,
#         s.alignment_resources = $alignment_resources,
#         s.alignment_activities = $alignment_activities,
#         s.alignment_culture = $alignment_culture,
#         s.alignment_outputs = $alignment_outputs,
#         s.alignment_outcomes = $alignment_outcomes,
#         s.context_score = $context_score,
#         s.processes_score = $processes_score,
#         s.interventions_and_research_score = $interventions_and_research_score,
#         s.engaged_learners_score = $engaged_learners_score,
#         s.outcomes_score = $outcomes_score
#     """
#     tx.run(query, **preferences)

# if __name__ == "__main__":
#     initiate_survey()
