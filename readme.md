# Office Schedule Streamlit App

This is a simple Streamlit web application that calculates and displays your office schedule based on a rotating team day and an optional second office day. The team day calculation starts from **Monday, March 31, 2025**, and rotates one day each month.

## Features:
- **Automatic Calculation**: The team day starts on Monday and rotates by one day each month.
- **Second Office Day Logic**: Based on the team day, the second office day is determined with specific rules.
- **Manual Override**: You can pass a CLI argument to manually set the second office day.

## Requirements
- Python 3.x
- Streamlit library

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/office-schedule-app.git
   cd office-schedule-app
2. Install the required Python libraries:

    ```bash
    pip install streamlit
**Note**: It is recommended to make use of a virtual environment when using python. For more info visit the [streamlit install](https://docs.streamlit.io/get-started/installation/command-line) website.

## Usage
### Run the Streamlit App (Default Mode)

To run the app with the automatic calculation of the team day and the second office day:
    
    streamlit run app.py

This will start a local web server, and the application will be available in your browser. The app will display the calculated team day for the current month, along with the second office day based on the rules.
### Manually Set the Second Office Day (CLI Mode)

To manually set the second office day (e.g., if you want to override the automatic calculation), you can pass the --second-office-day argument.

For example, to set the second office day to Tuesday, run the following command:

streamlit run app.py -- --second-office-day Tuesday

Make sure to include the -- before the argument to separate the Streamlit options from your custom arguments.

### Team day Rotation Logic

    The team day starts as Monday, March 31, 2025, and rotates forward by one day each month. The team day calculation uses this start date as the reference point.

    The second office day is calculated based on the following rules:

        If the team day is Monday, the second day will be Wednesday.

        If the team day is Tuesday, the second day will be Thursday.

        If the team day is Wednesday, the second day will be Monday.

        If the team day is Thursday, the second day will be Tuesday.

        If the team day is Friday, the second day will be Wednesday.

#### Example

If the team day is Monday, the app will automatically set the second office day to Wednesday. You can also manually change the second office day using the --second-office-day argument.

If running via docker, run via the following command: **docker run --rm -d -p 8080:8501 streamlit-office-schedule:1.1**

**Info**: You can make use of the optional arg `--second-office-day` by passing `-- --second-office-day Thursday` for example.

### Extra
This is was a fun, requested side project.