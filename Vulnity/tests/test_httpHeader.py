# tests/test_http_header.py

import requests

# Define payloads for HTTP header injection tests
header_injection_payloads = ["test\r\nX-injected-header: Injected", "Content-Length: 0\r\n\r\n<script>alert('Injected')</script>"]

def test_http_header_injection(url):
    results = []
    for payload in header_injection_payloads:
        sanitized_payload = payload.replace("\r", "").replace("\n", "")
        headers = {"User-Agent": sanitized_payload}
        response = requests.get(url, headers=headers)
        if "Injected" in response.text or "alert" in response.text:
            results.append({"payload": payload, "vulnerable": True, "reason": "HTTP header content reflected in response."})
    return results
