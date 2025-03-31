# Use an official Python runtime as a parent image
FROM python:3.13

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip

# Install the required dependencies
RUN pip install streamlit pandas

# Expose the port Streamlit will run on
EXPOSE 8501

# Define the command to run your Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py"]
