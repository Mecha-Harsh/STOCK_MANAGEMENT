import requests

# URL of the Flask app
url = 'http://127.0.0.1:5000/login'

# Data to be sent in the POST request
data = {
    'username': 'testuser'  # Example username
}

# Sending POST request
response = requests.post(url, data=data)

# Print the response
print(response.text)
