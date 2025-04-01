import os
import time
import threading
import requests
import schedule
import snowflake.connector

# Configuration
TOKEN_URL = "TOKEN ENDPOINT"
CLIENT_ID = "CLIENT ID"
CLIENT_SECRET = os.getenv("OKTA_CLIENT_SECRET")  # environment variable
SCOPE = "session:role:sysadmin" # customer defined role assumed (AuthZ)

# Validate that CLIENT_SECRET is set
if not CLIENT_SECRET:
    raise ValueError("Missing CLIENT_SECRET. Ensure OKTA_CLIENT_SECRET environment variable is set.")

# Function to obtain an access token
def get_access_token():
    response = requests.post(
        TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "client_credentials", "scope": SCOPE},
        auth=(CLIENT_ID, CLIENT_SECRET),
    )

    if response.status_code != 200:
        print("Error Response:", response.text)  # Print error
        raise requests.exceptions.HTTPError(f"Failed to get token: {response.text}")

    return response.json()["access_token"]

# Variable for the access token
access_token = None

# Function to request the access token flow
def request_token():
    global access_token
    try:
        access_token = get_access_token()
        print(f"New token acquired: {access_token}")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to acquire access token: {e}")

# Schedule token request every 5 minutes
schedule.every(5).minutes.do(request_token)

# Function to create a Snowflake connection
def create_snowflake_connection():
    global access_token
    if not access_token:
        raise ValueError("Access token request failed")
    return snowflake.connector.connect(
        user=CLIENT_ID,
        account="SF_ACCOUNT",
        warehouse="AZURE",
        database="DG_DEMO",
        schema="GOVERNANCE_DEMO",
        authenticator="OAUTH",
        token=access_token,
    )

# Run the scheduler in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler in the background
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# Create an initial Snowflake connection
try:
    # Ensure the first token is obtained before using it
    if access_token is None:
        access_token = get_access_token()
        print(f"Initial token acquired: {access_token}")

    conn = create_snowflake_connection()
    print("Connected to Snowflake via OAuth")
    
    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_TIMESTAMP();")
    result = cursor.fetchall()
    print(result)
    
finally:
    cursor.close()
    conn.close()
    print("Snowflake connection closed.")
