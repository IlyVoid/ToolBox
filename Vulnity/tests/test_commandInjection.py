# tests/test_command_injection.py

import requests

# Define payloads for command injection tests
command_injection_payloads = ["; ls", "&& cat /etc/passwd", "| whoami"]

def test_command_injection(url):
    """
    Tests for command injection vulnerabilities by injecting a variety of payloads into the URL.
    The function checks the response for signs of command execution (e.g., 'root' or 'user' in the response body).
    
    :param url: Target URL to test.
    :return: A list of results, each indicating whether a payload resulted in a vulnerability.
    """
    results = []
    for payload in command_injection_payloads:
        target = f"{url}?cmd={payload}"
        
        try:
            # Send the HTTP request with the payload
            response = requests.get(target)
            # Check if the response contains evidence of command execution (like 'root' or 'user')
            if "root" in response.text or "user" in response.text:
                results.append({
                    "payload": payload,
                    "vulnerable": True,
                    "reason": "Command execution detected in response."
                })
            else:
                results.append({
                    "payload": payload,
                    "vulnerable": False,
                    "reason": "No command execution detected."
                })
        except requests.exceptions.RequestException as e:
            # Handle any HTTP request errors (timeouts, connection issues, etc.)
            results.append({
                "payload": payload,
                "vulnerable": False,
                "reason": f"Request failed: {e}"
            })
    
    return results
