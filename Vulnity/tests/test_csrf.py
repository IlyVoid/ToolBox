# tests/test_csrf.py

import requests

# Define payloads for CSRF tests
csrf_payloads = [
    {"url": "/update-profile", "data": {"name": "Hacked User"}, "method": "POST"},
    {"url": "/change-password", "data": {"password": "newpassword123"}, "method": "POST"},
    {"url": "/delete-account", "data": {"confirm": "yes"}, "method": "POST"}
]

def test_csrf(url):
    """
    Tests for CSRF vulnerabilities by attempting to perform state-changing actions
    on the target URL without the necessary authentication or anti-CSRF tokens.
    
    :param url: The base target URL to test for CSRF vulnerabilities.
    :return: A list of results, each indicating whether the target is vulnerable to CSRF for a specific endpoint.
    """
    results = []
    
    for payload in csrf_payloads:
        target = url + payload["url"]
        
        try:
            # Send the POST request to the target URL with the payload data
            response = requests.post(target, data=payload["data"], allow_redirects=False)
            
            # Check for a successful response indicating that the state was potentially changed
            if response.status_code == 200:
                # Check if the response contains elements that might indicate a successful state change
                results.append({
                    "payload": f"{payload['url']} with data {payload['data']}",
                    "vulnerable": True,
                    "reason": f"CSRF possible on state-changing request. Status code: {response.status_code}."
                })
            else:
                results.append({
                    "payload": f"{payload['url']} with data {payload['data']}",
                    "vulnerable": False,
                    "reason": f"No CSRF vulnerability detected. Status code: {response.status_code}."
                })
        except requests.exceptions.RequestException as e:
            # Handle network errors (e.g., timeout, connection error)
            results.append({
                "payload": f"{payload['url']} with data {payload['data']}",
                "vulnerable": False,
                "reason": f"Request failed: {e}"
            })
    
    return results
