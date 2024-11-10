# tests/test_idor.py

import requests

def test_idor(url, test_ids=None):
    """
    Tests for Insecure Direct Object Reference (IDOR) vulnerabilities by accessing user profiles 
    with different user IDs and checking for unauthorized data access.

    :param url: The base target URL to test for IDOR vulnerabilities.
    :param test_ids: A list of user IDs to test for IDOR vulnerabilities (default is [1, 2]).
    :return: A list of results indicating whether the target is vulnerable to IDOR for each user profile.
    """
    
    # Default user IDs if not provided
    if test_ids is None:
        test_ids = [1, 2]
    
    results = []
    
    for test_id in test_ids:
        try:
            # Construct the target URL to access user profile
            target_url = f"{url}/users/{test_id}/profile"
            
            # Send GET request to the target URL
            response = requests.get(target_url)
            
            # Check for potential unauthorized access based on response content
            if response.status_code == 200 and any(keyword in response.text.lower() for keyword in ["username", "email", "profile"]):
                results.append({
                    "payload": f"Accessing /users/{test_id}/profile",
                    "vulnerable": True,
                    "reason": f"Unauthorized access to profile data. Status code: {response.status_code}."
                })
            else:
                results.append({
                    "payload": f"Accessing /users/{test_id}/profile",
                    "vulnerable": False,
                    "reason": f"No unauthorized access detected. Status code: {response.status_code}."
                })
        
        except requests.exceptions.RequestException as e:
            # Handle network-related errors and add them to results
            results.append({
                "payload": f"Accessing /users/{test_id}/profile",
                "vulnerable": False,
                "reason": f"Request failed: {e}"
            })
    
    return results
