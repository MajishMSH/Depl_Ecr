import os
import time
from datetime import datetime, timedelta
import requests

# Function to check the last modification time of the file
def check_file_modification(file_path):
    if os.path.exists(file_path):
        modification_time = os.path.getmtime(file_path)
        return datetime.fromtimestamp(modification_time)
    else:
        return None

# Function to send a message to Microsoft Teams via webhook
def send_teams_message(webhook_url, message):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "text": message
    }
    response = requests.post(webhook_url, headers=headers, json=data)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")

# Path to the log file
file_path = 'D:\\Putty log\\10.9.50.32-20241207-010957.log'

# Microsoft Teams webhook URL
webhook_url = 'your_webhook_url'

# Time interval to check for file modification (in seconds)
check_interval = 300  # Check every 5 minutes

# Variable to track the last alert time
last_alert_time = None

while True:
    last_modification_time = check_file_modification(file_path)
    if last_modification_time:
        current_time = datetime.now()
        if current_time - last_modification_time > timedelta(minutes=5):
            if last_alert_time is None or current_time - last_alert_time > timedelta(minutes=5):
                send_teams_message(
                    webhook_url="https://cholainvest.webhook.office.com/webhookb2/a86c4d70-4d8a-40e0-b6dd-8ec83bc56ef8@370ba3da-1a7a-440e-a7a7-b857f46e8f6e/IncomingWebhook/68e11f97f6fe45a58efcb51466a86eae/7133cce7-2fb2-4f3a-9cfc-4191d21994fd/V2lHEnVX16Zp6p2c9Wb3avJiFfZTvD_HHfCYGrjh4GiHk1",
                    message=f"Alert: 3par upgrade alert, The file {file_path} has not been modified for more than 5 minutes."
                )
                last_alert_time = current_time
    time.sleep(check_interval)