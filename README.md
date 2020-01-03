# work-scheduler

Work-Scheduler is a python script that watches a user's GMAIL inbox for an attached work schedule PDF, parses it for necessary 
user information and automatically sends back an .ics (iCal) file for the user to add to their preferred online 
calendar/organizer.

This project is hosted as a lambda function on the Google Cloud Platform, using the GMAIl API and a pdf-converter (ZamZar) API.


The script uses OAUTH tokens for authentication user acknowledgement for permissions with using GMAIL information.
