# main.py

import os
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table  # Import Table from rich
from styles.console_utils import console, display_results
from styles.report_utils import generate_report

# Import test functions from the modularized test files
from tests.test_sql import test_sql_injection
from tests.test_xss import test_xss
from tests.test_traversal import test_directory_traversal
from tests.test_idor import test_idor
from tests.test_csrf import test_csrf
from tests.test_commandInjection import test_command_injection
from tests.test_httpHeader import test_http_header_injection

# Function to map test numbers to functions and names
TESTS = {
    "1": ("SQL Injection", test_sql_injection),
    "2": ("XSS", test_xss),
    "3": ("Directory Traversal", test_directory_traversal),
    "4": ("IDOR", test_idor),
    "5": ("CSRF", test_csrf),
    "6": ("Command Injection", test_command_injection),
    "7": ("HTTP Header Injection", test_http_header_injection),
}

def run_test(test_func, url):
    """Run a given test function on the specified URL."""
    return test_func(url)

def show_menu():
    # Create reports directory if it doesn't exist
    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    while True:
        console.print(Panel("Vulnity powered on...", style="bold green"))
        url = Prompt.ask("[bold blue]Enter the target URL")

        # Create and display the tests table
        table = Table(title="Available Tests")
        table.add_column("No.", style="cyan", justify="center")
        table.add_column("Test Name", style="magenta")

        for num, (name, _) in TESTS.items():
            table.add_row(num, name)

        console.print(table)

        # Get selected tests by number
        selected_tests = Prompt.ask("[bold yellow]Select tests to run (comma-separated numbers)").split(',')
        selected_tests = [test.strip() for test in selected_tests if test.strip() in TESTS]

        console.print(Panel(f"Scanning {url}...", style="bold cyan"))
        results = {}

        with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
            for test_num in selected_tests:
                test_name, test_func = TESTS[test_num]
                progress.add_task(description=f"Testing {test_name}...", total=None)
                results[test_name] = run_test(test_func, url)

        display_results(results)

        # Generate and save the report
        report_content = generate_report(url, results)
        report_filename = f"reports/{url.replace('http://', '').replace('https://', '').replace('/', '_')}_report.txt"
        with open(report_filename, "w") as report_file:
            report_file.write(report_content)

        console.print(f"\n[bold green]Report saved to 'reports' folder.\n")
        
        another_scan = Prompt.ask("[bold blue]Run another scan? (y/n)")
        if another_scan.lower() != 'y':
            break

if __name__ == "__main__":
    show_menu()
