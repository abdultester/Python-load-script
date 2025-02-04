import requests
import concurrent.futures
import time

# Define the API endpoints
ACCESS_TOKEN_URL = 'https://api.thisisblowingmymind.com.au/api/v1/login/access-token'
TEST_TOKEN_URL = 'https://api.thisisblowingmymind.com.au/api/v1/login/test-token'
REFRESH_TOKEN_URL = 'https://api.thisisblowingmymind.com.au/api/v1/login/refresh-token'
GOOGLE_URL = 'https://api.thisisblowingmymind.com.au/api/v1/login/google'
GOOGLE_CALLBACK_URL = 'https://api.thisisblowingmymind.com.au/api/v1/login/google/callback'

# Function to get access token
def get_access_token():
    data = {
        'grant_type': '',
        'username': '', #add user name
        'password': '', #add password 
        'scope': '',
        'client_id': '',
        'client_secret': ''
    }
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(ACCESS_TOKEN_URL, headers=headers, data=data)
    return response

# Function to get test token using the access token
def get_test_token(access_token):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(TEST_TOKEN_URL, headers=headers)
    
    # Check if the response is empty or not JSON
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print(f"Error parsing JSON for {response.url}: {response.text}")
            return None
    else:
        print(f"Error: {response.status_code}, Response: {response.text}")
        return None

# Function to refresh the access token
def refresh_access_token(access_token):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(REFRESH_TOKEN_URL, headers=headers)
    return response

# Function to call Google login
def call_google_login():
    headers = {
        'accept': 'application/json'
    }
    response = requests.get(GOOGLE_URL, headers=headers)
    return response

# Function to call Google callback
def call_google_callback():
    headers = {
        'accept': 'application/json'
    }
    response = requests.get(GOOGLE_CALLBACK_URL, headers=headers)
    return response

# Load test function
def load_test(num_requests):
    start_time = time.time()
    access_token_response = get_access_token()
    
    if access_token_response.status_code == 200:
        access_token = access_token_response.json().get('access_token')
        print(f"Access Token: {access_token}")

        # Use ThreadPoolExecutor to send multiple requests concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            # Test Token Requests
            for _ in range(num_requests):
                futures.append(executor.submit(get_test_token, access_token))
            # Refresh Token Requests
            for _ in range(num_requests):
                futures.append(executor.submit(refresh_access_token, access_token))
            # Google Login Requests
            for _ in range(num_requests):
                futures.append(executor.submit(call_google_login))
            # Google Callback Requests
            for _ in range(num_requests):
                futures.append(executor.submit(call_google_callback))

            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    print(f"Response Code: {response.status_code}, Response: {response.json()}")
                except Exception as e:
                    print(f"Request generated an exception: {e}")

    else:
        print(f"Failed to get access token: {access_token_response.status_code}, {access_token_response.json()}")

    duration = time.time() - start_time
    print(f"Load test completed in {duration:.2f} seconds.")

# Run the load test with the desired number of requests
if __name__ == "__main__":
    load_test(10)  # Change the number to the desired load
