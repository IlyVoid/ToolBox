# tests/test_idor.py

import requests

def test_idor(url, test_ids=[1, 2]):
    results = []
    for test_id in test_ids:
        response = requests.get(f"{url}/users/{test_id}/profile")
        if response.status_code == 200 and any(keyword in response.text.lower() for keyword in ["username", "email", "profile"]):
            results.append({"payload": f"Accessing /users/{test_id}/profile", "vulnerable": True, "reason": "Unauthorized access to profile data."})
        else:
            results.append({"payload": f"Accessing /users/{test_id}/profile", "vulnerable": False, "reason": "No unauthorized access detected."})
    return results
