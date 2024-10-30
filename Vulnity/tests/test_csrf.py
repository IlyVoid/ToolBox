# tests/test_csrf.py

import requests

# Define payloads for CSRF tests
csrf_payloads = [{"url": "/update-profile", "data": {"name": "Hacked User"}, "method": "POST"}]

def test_csrf(url):
    results = []
    for payload in csrf_payloads:
        target = url + payload["url"]
        response = requests.post(target, data=payload["data"], allow_redirects=False)
        if response.status_code == 200:
            results.append({"payload": f"{payload['url']} with data {payload['data']}", "vulnerable": True, "reason": "CSRF possible on state-changing request."})
    return results
