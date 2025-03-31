import streamlit as st
import argparse
from datetime import datetime
import pandas as pd

# Function to calculate the teamday, starting from Monday, March 31, 2025
def calculate_teamday():
    # Starting date is Monday, March 31, 2025
    start_date = datetime(2025, 3, 31)
    
    # Get the current month
    current_date = datetime.now()
    
    # The teamday starts on Monday, March 31, 2025, and will rotate each month
    # Calculate how many months have passed since March 2025
    months_diff = (current_date.year - start_date.year) * 12 + current_date.month - start_date.month
    
    # Teamday rotates by one day for each month
    # Define the starting weekday as Monday (0=Monday, ..., 6=Sunday)
    teamday_offset = months_diff % 7
    
    # The weekdays list
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Calculate the teamday by rotating the weekday
    teamday = weekdays[teamday_offset]
    
    return teamday

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
            "teamday_label": "Your team day for this month is: ",
            "second_office_day_label": "Your second office day for this week is: ",
            "note": "This day may vary depending on circumstances",
            "table_header": ["Type of office day", "Day"],
            "teamday": "Team day",
            "second_office_day": "Second Office Day"
        },
        "fr": {
            "title": "Horaire du bureau",
            "teamday_label": "Votre jour d'équipe pour ce mois est: ",
            "second_office_day_label": "Votre deuxième jour de bureau pour cette semaine est : ",
            "note": "Ce jour peut varier en fonction des circonstances",
            "table_header": ["Jour", "Date"],
            "teamday": "Jour d'équipe",
            "second_office_day": "Deuxième jour de bureau"
        },
        "nl": {
            "title": "Kantoorrooster",
            "teamday_label": "Je teamdag voor deze maand is: ",
            "second_office_day_label": "Je tweede kantoordag voor deze week is: ",
            "note": "Deze dag kan variëren afhankelijk van omstandigheden",
            "table_header": ["Type kantoor dag", "Dag"],
            "teamday": "Teamdag",
            "second_office_day": "Tweede kantoordag"
        }
    }
    
    return translations.get(language, translations["en"])

# Function to display the office days based on teamday and CLI argument
def display_office_days():    
    # Parse CLI arguments
    args = parse_args()
        
    # Calculate the teamday for the current month
    teamday = calculate_teamday()
    
    # If a second office day is provided via CLI, use it; otherwise, calculate it
    if args.second_office_day:
        second_office_day = args.second_office_day
    else:
        second_office_day = get_second_office_day(teamday)
    
    # Get the selected language from the sidebar
    language = st.sidebar.selectbox(
        "Select your language",
        ("English", "Français", "Nederlands")
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
    
    # Display the results
    st.title(translations["title"])
    st.write(f"{translations['teamday_label']}**{teamday}**")
    st.write(f"{translations['second_office_day_label']}**{second_office_day}**")
    st.write(f"**Note**: {translations['note']}")

    # Display the days in a table (convert dictionary to DataFrame)
    office_schedule = {
        translations["table_header"][0]: [translations["teamday"], translations["second_office_day"]],
        translations["table_header"][1]: [teamday, second_office_day]
    }
    
    # Create a DataFrame and set index=False to remove the index column
    df = pd.DataFrame(office_schedule)
    
    # Display the table without the index column
    st.dataframe(df, hide_index=True)

# Create the Streamlit page
def main():
    display_office_days()

if __name__ == "__main__":
    main()
