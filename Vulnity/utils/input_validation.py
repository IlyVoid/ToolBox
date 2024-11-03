import re

def validate_url(url):
    pattern = re.compile(r'^(http|https)://')
    return bool(pattern.match(url))

def validate_test_selection(selection, available_tests):
    return all(test in available_tests for test in selection)
