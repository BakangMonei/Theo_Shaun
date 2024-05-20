import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import pycountry
import csv
import random
from datetime import datetime, timedelta
import os

# Utility Functions
def generate_test_data(num_records=100):
    # Generating test data for web server logs
    athletes = ["Athlete " + str(i) for i in range(1, 21)]
    sports = ["Sport " + str(i) for i in range(1, 6)]
    countries = [country.name for country in pycountry.countries]
    
    data = []
    for _ in range(num_records):
        timestamp = datetime.now() - timedelta(days=random.randint(0, 365))
        ip_address = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        country = random.choice(countries)
        athlete = random.choice(athletes)
        sport = random.choice(sports)
        age = random.randint(18, 40)
        gender = random.choice(['Male', 'Female'])
        nationality = country
        match_date = timestamp + timedelta(days=random.randint(1, 30))
        outcome = random.choice(['Win', 'Loss', 'Draw'])
        medals = random.choice(['Gold', 'Silver', 'Bronze', 'None'])
        rank = random.randint(1, 100)
        stadium = "Stadium " + str(random.randint(1, 10))
        height = round(random.uniform(1.5, 2.0), 2)
        weight = round(random.uniform(50.0, 100.0), 2)
        competition_date = timestamp
        
        data.append([timestamp, ip_address, country, athlete, sport, age, gender, nationality, match_date, outcome, medals, rank, stadium, height, weight, competition_date])
    
    columns = ["Timestamp", "IP Address", "Country", "Athlete Name", "Sport", "Age", "Gender", "Nationality", "Match Date", "Outcome", "Medals", "Rank", "Stadium", "Height", "Weight", "Competition Date"]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('test_data.csv', index=False)
    return df

def generate_web_logs(num_records=100):
    # Generating web logs
    countries = [country.name for country in pycountry.countries]
    interests = ["Interest " + str(i) for i in range(1, 6)]
    devices = ["Mobile", "Desktop", "Tablet"]
    
    logs = []
    for _ in range(num_records):
        country = random.choice(countries)
        visits = random.randint(1, 20)
        visit_times = [datetime.now() - timedelta(days=random.randint(0, 365)) for _ in range(visits)]
        interest = random.choice(interests)
        device = random.choice(devices)
        ip_address = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        for visit_time in visit_times:
            logs.append([country, visit_time, interest, device, ip_address])
    
    columns = ["Country of Origin", "Visit Time", "Main Interest", "Device Used", "IP Address"]
    log_df = pd.DataFrame(logs, columns=columns)
    log_df.to_csv('web_logs.csv', index=False)
    return log_df

def authenticate(username, password):
    # Basic user authentication
    if os.path.exists('users.csv'):
        with open('users.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row == [username, password]:
                    return True
    return False

def register_user(username, password):
    if not os.path.exists('users.csv'):
        with open('users.csv', mode='w') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])
    else:
        with open('users.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])

# Streamlit Pages
def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

def register_page():
    st.title("Register Page")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type='password')
    if st.button("Register"):
        register_user(new_username, new_password)
        st.success("User registered successfully!")

def analysis_page():
    st.title("Web Server Log Analysis Tool")
    
    num_records = st.number_input("Enter number of records to generate", min_value=10, max_value=10000, value=100, step=10)
    
    data = generate_test_data(num_records)
    web_logs = generate_web_logs(num_records)
    
    st.header("Generated Test Data")
    st.write(data.head())
    
    st.header("Generated Web Logs")
    st.write(web_logs.head())
    
    st.header("Analysis and Visualization")
    
    # Grid layout for charts
    fig_col1, fig_col2, fig_col3 = st.columns(3)
    fig_col4, fig_col5, fig_col6 = st.columns(3)
    fig_col7, fig_col8, fig_col9 = st.columns(3)
    fig_col10 = st.columns(1)[0]
    
    with fig_col1:
        # Bar chart for visits by country
        visit_counts = web_logs["Country of Origin"].value_counts()
        fig1 = plt.figure()
        plt.bar(visit_counts.index, visit_counts.values)
        plt.xlabel('Country')
        plt.ylabel('Number of Visits')
        plt.title('Visits by Country')
        st.pyplot(fig1)
    
    with fig_col2:
        # Pie chart for devices used
        device_counts = web_logs["Device Used"].value_counts()
        fig2 = px.pie(values=device_counts.values, names=device_counts.index, title='Devices Used')
        st.plotly_chart(fig2)
    
    with fig_col3:
        # Scatter plot for age vs. height
        fig3 = px.scatter(data, x='Age', y='Height', color='Gender', title='Age vs. Height')
        st.plotly_chart(fig3)
    
    with fig_col4:
        # Bar chart for sports distribution
        sport_counts = data["Sport"].value_counts()
        fig4 = plt.figure()
        plt.bar(sport_counts.index, sport_counts.values)
        plt.xlabel('Sport')
        plt.ylabel('Number of Athletes')
        plt.title('Athletes by Sport')
        st.pyplot(fig4)
    
    with fig_col5:
        # Pie chart for outcomes
        outcome_counts = data["Outcome"].value_counts()
        fig5 = px.pie(values=outcome_counts.values, names=outcome_counts.index, title='Match Outcomes')
        st.plotly_chart(fig5)
    
    with fig_col6:
        # Histogram for athlete ages
        fig6 = plt.figure()
        plt.hist(data['Age'], bins=10, color='skyblue', edgecolor='black')
        plt.xlabel('Age')
        plt.ylabel('Number of Athletes')
        plt.title('Age Distribution of Athletes')
        st.pyplot(fig6)
    
    with fig_col7:
        # Line chart for rank over time
        data['Match Date'] = pd.to_datetime(data['Match Date'])
        rank_over_time = data.groupby(data['Match Date'].dt.to_period("M"))['Rank'].mean().reset_index()
        rank_over_time['Match Date'] = rank_over_time['Match Date'].dt.to_timestamp()
        fig7 = px.line(rank_over_time, x='Match Date', y='Rank', title='Average Rank Over Time')
        st.plotly_chart(fig7)
    
    with fig_col8:
        # Box plot for athlete weights by sport
        fig8 = px.box(data, x='Sport', y='Weight', color='Sport', title='Athlete Weights by Sport')
        st.plotly_chart(fig8)
    
    with fig_col9:
        # Histogram for match dates
        fig9 = plt.figure()
        plt.hist(data['Match Date'].dt.to_pydatetime(), bins=10, color='green', edgecolor='black')
        plt.xlabel('Match Date')
        plt.ylabel('Number of Matches')
        plt.title('Distribution of Match Dates')
        st.pyplot(fig9)
    
    with fig_col10:
        # Bar chart for gender distribution
        gender_counts = data["Gender"].value_counts()
        fig10 = plt.figure()
        plt.bar(gender_counts.index, gender_counts.values, color=['blue', 'pink'])
        plt.xlabel('Gender')
        plt.ylabel('Number of Athletes')
        plt.title('Gender Distribution of Athletes')
        st.pyplot(fig10)
    
    # Exporting data
    st.header("Export Data")
    if st.button("Export Test Data as CSV"):
        data.to_csv('exported_test_data.csv', index=False)
        st.success("Test data exported successfully!")
    if st.button("Export Web Logs as CSV"):
        web_logs.to_csv('exported_web_logs.csv', index=False)
        st.success("Web logs exported successfully!")
        
# Main
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

st.sidebar.title("Navigation")
if st.session_state['logged_in']:
    page = st.sidebar.selectbox("Choose a page", ["Analysis Tool", "Logout"])
    if page == "Analysis Tool":
        analysis_page()
    elif page == "Logout":
        st.session_state['logged_in'] = False
        st.success("Logged out successfully!")
else:
    page = st.sidebar.selectbox("Choose a page", ["Login", "Register"])
    if page == "Login":
        login_page()
    elif page == "Register":
        register_page()
