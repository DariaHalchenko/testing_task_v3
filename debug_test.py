import requests

MEASUREMENT_ID = "G-BDEF2MYY8F"
API_SECRET = "5kVYOJJiSPurqL8UoxRhFA" 
CLIENT_ID = "debugtest12345"

payload = {
    "client_id": CLIENT_ID,
    "events": [{"name": "test_event"}]
}

url = f"https://www.google-analytics.com/debug/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}"

response = requests.post(url, json=payload)
print(response.status_code, response.text)
