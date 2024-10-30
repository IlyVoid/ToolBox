# tests/test_xss.py

import requests

# Define payloads for XSS tests
xss_payloads = ["<script>alert('XSS')</script>", "<img src='x' onerror='alert(1)'>", "<body onload=alert(1)>"]

def test_xss(url):
    results = []
    for payload in xss_payloads:
        target = f"{url}?q={payload}"
        response = requests.get(target)
        if payload in response.text:
            results.append({"payload": payload, "vulnerable": True, "reason": "Reflected payload detected in response, indicating potential XSS."})
    return results
