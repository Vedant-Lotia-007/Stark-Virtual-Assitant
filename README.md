# Stark Virtual Assistant

Stark is a virtual assistant created for understanding the basics of speech recognition during undergraduate coursework. It utilizes Python libraries like `pyttsx3`, `speech_recognition`, `wikipedia`, `webbrowser`, and others to perform various tasks through voice commands.

## Features
- Voice interaction using the `pyttsx3` and `speech_recognition` libraries.
- Can tell the current time and date.
- Can search Wikipedia and read the summary of the search out loud.
- Can open web browsers and search Google.
- Can send emails by taking the recipient's email and the content of the email through voice.
- Can play songs from a specified directory.
- Can open WhatsApp web and send messages.
- Can interact with MySQL databases.
- Capable of continuous interaction until told to stop.

## Prerequisites
- Python 3.x
- pyttsx3
- speech_recognition
- wikipedia
- webbrowser
- os, sys
- datetime
- googlesearch-python
- getpass4
- selenium
- re
- mysql-connector
- smtplib
- nltk

## Installation

1. Clone the repository to your local machine:
```bash
git clone https://github.com/your-username/Stark-virtual-assistant.git
cd Stark-virtual-assistant
```
- Install the required Python packages:

  ```bash
  pip install pyttsx3 speech_recognition wikipedia webbrowser googlesearch-python getpass4 selenium mysql-connector-python smtplib nltk
  ```
  
- Make sure you have Firefox installed, as the selenium package in this project is configured to use Firefox.
- Start interacting with Stark by running:

  ```bash
  python Stark Virtual Assistant.py
  ```

## Usage
1. Run the script, and Stark will greet you according to the time of day and ask how it can assist you.
2. Speak your command, such as asking for the time, date, or initiating other tasks like sending emails, or opening WhatsApp.
3. Stark will perform the task and then ask if there is anything else it can assist with.
4. To end the interaction, simply tell Stark 'no' when asked if there is anything else.

## Contact
For any questions or clarifications, feel free to reach out at vedantlotia007@gmail.com or raise an issue on this GitHub repository.
