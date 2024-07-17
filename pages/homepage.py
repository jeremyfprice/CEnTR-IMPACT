import streamlit as st

def app():
    st.title('Welcome to CEnTR*IMPACT')
    
    st.markdown("""
        ## Empowering Community-Engaged Research
    
        Welcome to CEnTR*IMPACT, your gateway to a more inclusive and transformative approach to evaluating community-engaged research projects. Our platform empowers you to measure the true impact of your work, emphasizing inclusivity, community engagement, and transformative outcomes. Whether you're a researcher, community leader, or organization, CEnTR*IMPACT offers metrics to help you assess and tell the story of your projects. 
    
        Discover how our innovative tools can support your efforts in creating meaningful and sustainable community change. Join us in our mission to foster collaborative and impactful research for a better world.
    """)

    st.header("Features")
    st.markdown("""
    - **Create Survey Link**: Generate unique links for your new research projects and gather essential data.
    - **Generate CEnTR*IMPACT Scores**: Input details about your project and obtain various impact scores to understand the effectiveness of your initiatives.
    - **Visualize Outcomes**: View charts and graphs that illustrate the impact and outcomes of your community-engaged research.
    """)

    st.header("Get Started")
    st.markdown("""
    - **Navigate**: Use the menu on the left to access different parts of the application and explore various functionalities.
    - **Learn More**: Dive deeper into our resources to understand how CEnTR*IMPACT can enhance your research methodology.
    """)

    st.markdown(f"""
        <a href="/create_project_page" target="_self">
            <button style="padding: 0.5em; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
                Go to Create Survey Page
            </button>
        </a>
        """, unsafe_allow_html=True)

