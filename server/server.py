import sys
import os
import time
from flask import Flask, request, jsonify, render_template_string
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Add the parent directory to sys.path to import from different folder
sys.path.append(os.path.abspath('../'))
from secret.config import SAMPLE_SPREADSHEET_ID, GOOGLE_SHEET_URL

app = Flask(__name__)

# Set up Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '../secret/key.json'

credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)

@app.route('/')
def index():
    # Add a timestamp parameter to prevent caching
    timestamp = int(time.time())
    google_sheet_url_with_timestamp = f"{GOOGLE_SHEET_URL}&t={timestamp}"

    # Beautified HTML template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GPS Tracking Sheet</title>
        <style>
            /* Your CSS styles */
        </style>
    </head>
    <body>
        <h1>GPS Tracking Data</h1>
        <iframe src="{google_sheet_url_with_timestamp}" width="80%" height="600" frameborder="0"></iframe>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/api/location', methods=['POST'])
def receive_location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    carbon_saved = data.get('carbonSaved')

    # Update Google Sheet
    sheet = service.spreadsheets()
    # Update longitude
    update_sheet(sheet, 'B2', [[longitude]])
    # Update latitude
    update_sheet(sheet, 'C2', [[latitude]])
    # Update carbon savings
    update_sheet(sheet, 'D2', [[carbon_saved]])

    print(f"Received location: Latitude {latitude}, Longitude {longitude}, Carbon Saved {carbon_saved} kg")
    return jsonify({"message": "Data received and sheet updated successfully"}), 200

def update_sheet(sheet, range_name, values):
    body = {
        'values': values
    }
    result = sheet.values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name,
        valueInputOption='USER_ENTERED', body=body).execute()
    print(f"{result.get('updatedCells')} cells updated.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
