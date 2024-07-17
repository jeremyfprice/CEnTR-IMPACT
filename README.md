# CER-BEANS v2.0

Updating the CER-BEANS Metrics

## Project Structure

```
.
├── app.py
├── database.cypher
├── images/
├── requirements.txt
├── utils/
│   ├── calculations.py
│   └── unique_id.py
└── pages/
    ├── create_project_page.py
    ├── homepage.py
    ├── initiate_survey.py
    ├── scores.py
    ├── survey_page.py
    └── visualizations.py
```

## Page Descriptions

- **create_project_page.py**: Creates and initializes projects for survey creation.
- **initiate_survey.py**: Starts the create survey form with basic details and provides unique keys to be saved for later use.
- **survey_page.py**: Actual survey page where researchers and community members fill out the surveys. Scores are calculated in real-time within this file.
- **scores.py**: Currently contains boilerplate code.
- **visualizations.py**: Currently contains boilerplate code.

## Setup and Installation

1. Create a Conda environment:
   ```
   conda create --name cer-beans python=3.8
   conda activate cer-beans
   ```

2. Create a `.env` file in the root directory and add the following variables:
   ```
   OPEN_CAGE_API_KEY=your_api_key_here
   NEO4J_URI=your_neo4j_uri_here
   NEO4J_USER=your_neo4j_username_here
   NEO4J_PASSWORD=your_neo4j_password_here
   ```

3. Create a Neo4j account:
   - Visit [https://console.neo4j.io/](https://console.neo4j.io/)
   - Create a free instance
   - Copy the connection details to your `.env` file

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the entire site, use the following command:

```
streamlit run app.py
```

## Contributing

[Add information about how to contribute to the project, if applicable]

## License

[Add license information here]

## Contact

[Add contact information or links to project resources]
