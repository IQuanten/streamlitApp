import streamlit as st
import argparse
from datetime import datetime, timedelta
import pandas as pd

# Function to calculate the teamday, starting from Monday, March 31, 2025
def calculate_teamday():
    # Starting date is Monday, March 31, 2025
    start_date = datetime(2025, 3, 31)
    
    # Get the current date
    current_date = datetime.now()
    
    # Calculate the difference in days
    days_diff = (current_date - start_date).days
    
    # Calculate the number of 4-week periods (28 days) that have passed
    weeks_diff = days_diff // 28
    
    # Teamday rotates by one day for each 4-week period
    # Define the starting weekday as Monday (0=Monday, ..., 6=Sunday)
    teamday_offset = weeks_diff % 7
    
    # The weekdays list
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Calculate the teamday by rotating the weekday
    teamday = weekdays[teamday_offset]
    
    return teamday, current_date

# Function to determine the second office day based on the teamday
def get_second_office_day(teamday):
    # Logic for the second non-teamday based on the teamday
    second_office_day_mapping = {
        'Monday': 'Wednesday',
        'Tuesday': 'Thursday',
        'Wednesday': 'Monday',
        'Thursday': 'Tuesday',
        'Friday': 'Wednesday'
    }
    
    return second_office_day_mapping.get(teamday, 'Unknown')

# Function to calculate the next team day date
def get_next_teamday_date(current_date, teamday):
    # Define the start date (March 31, 2025, which is a Monday)
    start_date = datetime(2025, 3, 31)
    
    # List of weekdays in the sequence of the team day cycle
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    # Calculate the number of 28-day periods that have passed since the start date
    days_diff = (current_date - start_date).days
    weeks_diff = days_diff // 28
    
    # Determine the current team day index
    teamday_index = weekdays.index(teamday)
    
    # Calculate the next team day index by moving forward in the cycle
    next_teamday_index = (teamday_index + 1) % 5  # Rotates to the next day in the cycle
    
    # Calculate the date of the next team day
    next_teamday_date = start_date + timedelta(days=(weeks_diff * 28) + next_teamday_index)
    
    # If the next teamday is today or in the past, we need to add 28 days to reach the next rotation
    if next_teamday_date <= current_date:
        next_teamday_date += timedelta(days=28)
    
    return next_teamday_date

# Function to handle command-line arguments for overriding the second office day
def parse_args():
    parser = argparse.ArgumentParser(description='Set the second office day manually.')
    parser.add_argument('--second-office-day', type=str, help='Manually set the second office day (e.g., "Monday", "Tuesday", etc.)')
    return parser.parse_args()

# Function to get the selected language and provide translations
def get_translations(language):
    translations = {
        "en": {
            "title": "Office Schedule",
            "teamday_label": "The current team day is: ",
            "second_office_day_label": "The second office day for this week is: ",
            "note": "The second office day may vary depending on circumstances",
            "table_header": ["Type of office day", "Day"],
            "teamday": "Team day",
            "second_office_day": "Second Office Day",
            "Monday": "Monday",
            "Tuesday": "Tuesday",
            "Wednesday": "Wednesday",
            "Thursday": "Thursday",
            "Friday": "Friday",
            "time_remaining": "Days remaining until the team day changes: ",
            "days": "day(s)"
        },
        "fr": {
            "title": "Horaire du bureau",
            "teamday_label": "La journée actuelle de l'équipe est: ",
            "second_office_day_label": "Le deuxième jour de bureau de cette semaine est: ",
            "note": "Le deuxième jour de bureau peut varier selon les circonstances",
            "table_header": ["Jour", "Date"],
            "teamday": "Jour d'équipe",
            "second_office_day": "Deuxième jour de bureau",
            "Monday": "Lundi",
            "Tuesday": "Mardi",
            "Wednesday": "Mercredi",
            "Thursday": "Jeudi",
            "Friday": "Vendredi",
            "time_remaining": "Jours restants avant le changement de jour d'équipe: ",
            "days": "jour(s)"
        },
        "nl": {
            "title": "Kantoorrooster",
            "teamday_label": "De huidige teamdag is: ",
            "second_office_day_label": "De tweede kantoordag voor deze week is: ",
            "note": "De tweede kantoordag kan variëren afhankelijk van de omstandigheden",
            "table_header": ["Type kantoor dag", "Dag"],
            "teamday": "Teamdag",
            "second_office_day": "Tweede kantoordag",
            "Monday": "Maandag",
            "Tuesday": "Dinsdag",
            "Wednesday": "Woensdag",
            "Thursday": "Donderdag",
            "Friday": "Vrijdag",
            "time_remaining": "Dagen tot de teamdag verandert: ",
            "days": "dag(en)"
        }
    }
    
    return translations.get(language, translations["nl"])

# Function to display the office days based on teamday and CLI argument
def display_office_days():    
    # Parse CLI arguments
    args = parse_args()
        
    # Calculate the teamday for the current month
    teamday, current_date = calculate_teamday()
    
    # If a second office day is provided via CLI, use it; otherwise, calculate it
    if args.second_office_day:
        second_office_day = args.second_office_day
    else:
        second_office_day = get_second_office_day(teamday)
    
    # Get the selected language from the sidebar
    language = st.sidebar.selectbox(
        "Select your language",
        ("Nederlands", "Français", "English")
    )

    # Convert the selected language to the appropriate key (en, fr, nl)
    language_map = {
        "English": "en",
        "Français": "fr",
        "Nederlands": "nl"
    }

    selected_language = language_map.get(language, "en")
    
    # Get the translations based on the selected language
    translations = get_translations(selected_language)
    
    # Calculate the next team day date
    next_teamday_date = get_next_teamday_date(current_date, teamday)

    # Calculate the time remaining until the next team day
    time_remaining_until_next_rotation = next_teamday_date - current_date

    # Display the results
    st.title(translations["title"])
    st.write(f"{translations['teamday_label']}**{translations[teamday]}**")
    st.write(f"{translations['second_office_day_label']}**{translations[second_office_day]}**")
    st.write(f"**Note**: {translations['note']}")
    
    # Display the days in a table (convert dictionary to DataFrame)
    office_schedule = {
        translations["table_header"][0]: [translations["teamday"], translations["second_office_day"]],
        translations["table_header"][1]: [translations[teamday], translations[second_office_day]]
    }
    
    # Create a DataFrame
    df = pd.DataFrame(office_schedule)
    
    # Display the table without the index column
    st.dataframe(df, hide_index=True)

    # Display time remaining until the team day changes
    days_remaining = time_remaining_until_next_rotation.days
    st.write(f"{translations['time_remaining']}**{days_remaining} {translations['days']}**")

# Create the Streamlit page
def main():
    display_office_days()

if __name__ == "__main__":
    main()
