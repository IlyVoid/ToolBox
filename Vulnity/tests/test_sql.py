# tests/test_sql.py

import requests

# Define payloads for SQL injection tests
sql_payloads = ["' OR '1'='1", "' OR 1=1 --", "' OR 'a'='a' --"]

def test_sql_injection(url):
    results = []
    for payload in sql_payloads:
        target = f"{url}?id={payload}"
        response = requests.get(target)
        if "syntax" in response.text.lower() or "mysql" in response.text.lower() or "error" in response.text.lower():
            results.append({"payload": payload, "vulnerable": True, "reason": "Error messages indicating SQL syntax issues."})
    return results
