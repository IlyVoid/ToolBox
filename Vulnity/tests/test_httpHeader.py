# tests/test_http_header.py

import requests

# Define payloads for HTTP header injection tests
header_injection_payloads = [
    "test\r\nX-injected-header: Injected", 
    "Content-Length: 0\r\n\r\n<script>alert('Injected')</script>",
    "X-Forwarded-For: 127.0.0.1\r\nX-Injected-Header: Attack"
]

def test_http_header_injection(url):
    """
    Tests for HTTP header injection vulnerabilities by attempting to inject headers into requests
    and evaluating the server's response to see if the injected content is reflected.

    :param url: The base target URL to test for HTTP header injection vulnerabilities.
    :return: A list of results indicating whether the target is vulnerable to HTTP header injection for each payload.
    """
    results = []
    
    for payload in header_injection_payloads:
        # Sanitize the payload to ensure it doesn't break the request format
        sanitized_payload = payload.replace("\r", "").replace("\n", "")
        
        # Construct headers with the payload
        headers = {"User-Agent": sanitized_payload}
        
        try:
            # Send a GET request with the manipulated headers
            response = requests.get(url, headers=headers)
            
            # Check if the injected payload is reflected in the response
            if "Injected" in response.text or "<script>" in response.text or "alert" in response.text:
                results.append({
                    "payload": payload,
                    "vulnerable": True,
                    "reason": f"HTTP header content reflected in response. Status code: {response.status_code}."
                })
            else:
                results.append({
                    "payload": payload,
                    "vulnerable": False,
                    "reason": f"No reflection of header content detected. Status code: {response.status_code}."
                })
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            results.append({
                "payload": payload,
                "vulnerable": False,
                "reason": f"Request failed: {e}"
            })
    
    return results
