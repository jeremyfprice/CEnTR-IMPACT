import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_sector_bar_chart():
    sectors = ["Health", "Education", "Governance", "Ecology", "Nutrition", "Development"]
    values = np.random.randint(10, 100, size=len(sectors))

    plt.figure(figsize=(10, 6))
    sns.barplot(x=sectors, y=values, palette="viridis")
    plt.title("Project Sector Involvement")
    plt.xlabel("Sectors")
    plt.ylabel("Involvement Level")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt

def create_engagement_pie_chart():
    labels = ['Daily', 'Weekly', 'Monthly', 'Yearly']
    sizes = np.random.randint(100, 1000, size=len(labels))

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("muted", n_colors=4))
    plt.title("Frequency of Engagement")
    return plt

def create_engagement_line_graph():
    months = range(1, 13)  # Months of the year
    engagement_hours = np.random.randint(1, 50, size=len(months))

    plt.figure(figsize=(10, 6))
    sns.lineplot(x=months, y=engagement_hours, marker='o', color='b')
    plt.title("Engagement Hours Over Time")
    plt.xlabel("Month")
    plt.ylabel("Engagement Hours")
    plt.grid(True)
    return plt

def app():
    st.title('Visualization Dashboard')

    st.subheader("Project Sector Involvement Bar Chart")
    st.pyplot(create_sector_bar_chart())

    st.subheader("Frequency of Engagement Pie Chart")
    st.pyplot(create_engagement_pie_chart())

    st.subheader("Engagement Hours Over Time Line Graph")
    st.pyplot(create_engagement_line_graph())

if __name__ == "__main__":
    app()
