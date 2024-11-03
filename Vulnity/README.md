# Vulnity

Vulnity is a powerful and flexible web vulnerability scanning tool designed to help security professionals, developers, and pentesters identify vulnerabilities in web applications. With a user-friendly interface and modular design, Vulnity simplifies the process of running various security tests, generating comprehensive reports, and helping users understand the security posture of their applications.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Test Functions](#test-functions)
- [Contribution](#contribution)
- [License](#license)
- [Contact](#contact)

## Features

- **Modular Test Design**: Easily add, modify, or remove test functions for different vulnerabilities.
- **User-Friendly Interface**: Utilizes the `rich` library for a clean and interactive console interface.
- **Comprehensive Reporting**: Automatically generates detailed reports of scan results in text format.
- **Custom Payloads**: Supports custom payloads for various types of tests to adapt to specific applications.
- **Progress Tracking**: Provides real-time feedback during scans with progress indicators.

## Requirements

- Python 3.7 or higher
- Required libraries:
  - python -m venv (env_name)
  - source (env_name)/bin/activate (Linux) / .\(env_name)\Scripts\activate (Windows)
  - pip install -r requirements.txt

You can install the required libraries using pip:

```bash
pip install requests rich
```
Installation

To get started with Vulnity, clone the repository to your local machine:

```bash

git clone https://github.com/IlyVoid/ToolBox.git
cd ToolBox/Vulnity
```
Usage

To run Vulnity, navigate to the directory containing the main.py file and execute it:

```bash

python main.py
```
You will be prompted to enter the target URL and select the tests you want to run. You can select multiple tests by entering their corresponding numbers, separated by commas.
Available Tests

    1. SQL Injection
    2. Cross-Site Scripting (XSS)
    3. Directory Traversal
    4. IDOR
    5. Cross-Site Request Forgery (CSRF)
    6. Command Injection
    7. HTTP Header Injection

After the scan completes, a report will be generated and saved in the reports folder.
Test Functions

Vulnity includes various test functions to assess common web vulnerabilities:

    SQL Injection: Tests for SQL injection vulnerabilities using predefined payloads.
    Cross-Site Scripting (XSS): Checks for reflected XSS vulnerabilities.
    Directory Traversal: Attempts to access sensitive files on the server.
    IDOR (Insecure Direct Object Reference): Tests for unauthorized access to user data.
    CSRF (Cross-Site Request Forgery): Checks for CSRF vulnerabilities on state-changing requests.
    Command Injection: Tests for command injection vulnerabilities in user inputs.
    HTTP Header Injection: Checks if HTTP headers can be manipulated to inject content.

Contribution

Contributions are welcome! If you would like to contribute to Vulnity, please fork the repository and submit a pull request. You can also open issues for feature requests or bug reports.
License

This project is licensed under the MIT License - see the LICENSE file for details.
