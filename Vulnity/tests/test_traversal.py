# tests/test_traversal.py

import requests

# Define payloads for directory traversal tests
traversal_payloads = ["../../../../etc/passwd", "../../../windows/system32/cmd.exe", "../../../../../../etc/shadow"]

def test_directory_traversal(url):
    results = []
    for payload in traversal_payloads:
        target = f"{url}/{payload}"
        response = requests.get(target)
        if "root:" in response.text or "system32" in response.text:
            results.append({"payload": payload, "vulnerable": True, "reason": "Sensitive system content exposed in response."})
    return results
