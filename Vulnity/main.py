import os
import time
import requests  # Make sure to import requests
import pyfiglet
import concurrent.futures
from colorama import Fore
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.console import Console
from rich.text import Text
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

# Import Utils
from utils.logging_utils import setup_logging
from utils.cache_utils import save_cache, load_cache
from utils.input_validation import validate_url
from utils.config_utils import load_endpoints

logger = setup_logging()

# function to map Actions
ACTIONS = {
    "1": ("Run tests"),
    "2": ("View reports"),
}

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

def detect_endpoints(base_url, endpoints):
    detected_endpoints = {}

    def request_endpoint(endpoint):
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url)
            if response.status_code in [200, 301, 302, 404]:
                logger.info(f"Endpoint {url} returned status {response.status_code}")
                return url, response.status_code
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking {url}: {e}")
            return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(request_endpoint, endpoints)
        
    detected_endpoints.update({url: status for url, status in results if url is not None})
    
    return detected_endpoints

def run_test(test_func, url):
    """Run a given test function on the specified URL."""
    return test_func(url)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_startup_message():
    console.print(Panel("Starting Vulnity... Please wait.", style="bold yellow"))
    time.sleep(1)  # Simulating startup delay 

def show_menu():
    # Create reports directory if it doesn't exist
    if not os.path.exists("reports"):
        os.makedirs("reports")

    clear_terminal()
    display_startup_message()

    console.print(Panel("Vulnity powered on...", style="bold green"))

    while True:

        # Create a table for the 1st options
        table1 = Table(title="[bold blue]Actions")
        table1.add_column("No.", style="bold blue", justify="center")
        table1.add_column("Action", style="bold yellow")

        for num, (name) in ACTIONS.items():
            table1.add_row(num, name)

        console.print(table1)


        # User selects whether to test or view reports
        action = Prompt.ask("\n[bold blue]Choose an action: ")

        clear_terminal()

        if action == "1":
            url = Prompt.ask("\n[bold blue]Enter the target URL")

            # Validate URL
            if not validate_url(url):
                console.print("[bold red]Invalid URL. Please try again.")
                continue

            # Check cache for previous results
            cached_results = load_cache(url)
            if cached_results:
                console.print("[bold green]Cached results found. Loading from cache.")
                display_results(cached_results["results"])
                use_cache = Prompt.ask("[bold blue]Use cached results? (y/n)").lower() == 'y'
                if use_cache:
                    continue

            clear_terminal()

            # Display the tests table
            table = Table(title="[bold cyan]Available Tests")
            table.add_column("No.", style="bold cyan", justify="center")
            table.add_column("Test Name", style="bold magenta")

            for num, (name, _) in TESTS.items():
                table.add_row(num, name)

            console.print(table)

            # Get selected tests by number
            selected_tests = Prompt.ask("[bold yellow]Select tests to run (comma-separated numbers)").split(',')
            selected_tests = [test.strip() for test in selected_tests if test.strip() in TESTS]

            # Check if any valid tests were selected
            if not selected_tests:
                console.print("[bold red]No valid tests selected. Please try again.")
                continue

            
            # Load endpoints from configuration
            common_endpoints = load_endpoints()
            detected_endpoints = detect_endpoints(url, common_endpoints)

            console.print(Panel(f"Scanning {url}...", style="bold cyan"))
            results = {}

            # Run selected tests with progress
            with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
                for test_num in selected_tests:
                    test_name, test_func = TESTS[test_num]
                    progress.add_task(description=f"Testing {test_name}...", total=None)
                    results[test_name] = run_test(test_func, url)

            clear_terminal()
            display_results(results)

            # Generate and save the report, including detected endpoints
            report_content = generate_report(url, results, detected_endpoints)
            report_filename = f"reports/{url.replace('http://', '').replace('https://', '').replace('/', '_')}_report.txt"
            try:
                with open(report_filename, "w") as report_file:
                    report_file.write(report_content)
                console.print(f"\n[bold green]Report saved to 'reports' folder as {report_filename}.\n")
            except IOError:
                console.print("[bold red]Failed to save the report. Please check file permissions.")

            # Cache the results
            save_cache(url, results)

            new_action = Prompt.ask("\n[bold blue]Do you wish to perform another action? (y/n)")
            if new_action.lower() != 'y':
                break

            clear_terminal()
            
        elif action == "2":
            # List existing reports
            reports = os.listdir("reports")
            if not reports:
                console.print("[bold red]No reports found.")
            else:
                # Display reports in a numbered table
                table = Table(title="[bold blue]Available Reports", show_header=True, header_style="bold cyan")
                table.add_column("No.", style="bold yellow", justify="center")
                table.add_column("Report Name", style="bold green")
        
                for idx, report in enumerate(reports, start=1):
                    table.add_row(str(idx), report)
        
                console.print(table)

                # Option to view a specific report by number
                while True:
                    view_report = Prompt.ask("\n[bold yellow]Do you want to view a specific report? (y/n)")
                    if view_report.lower() not in ('y', 'n'):
                        console.print("[bold red]Invalid input. Please enter 'y' or 'n'.")
                        continue  # Re-prompt until correct input is received

                    if view_report.lower() == 'y':
                        try:
                            report_number = int(Prompt.ask("[bold blue]Enter the report number"))
                            if 1 <= report_number <= len(reports):
                                report_to_view = reports[report_number - 1]
                                report_path = os.path.join("reports", report_to_view)

                                clear_terminal()

                                if os.path.exists(report_path):
                                    try:
                                        with open(report_path, "r") as f:
                                            report_content = f.read()
                                        console.print(Panel(report_content, title=f"[bold cyan]{report_to_view}[/bold cyan]", style="bold green"))
                                    except IOError:
                                        console.print("[bold red]Failed to read the report. Please check file permissions.")
                                else:
                                    console.print("[bold red]Report not found. Please check the name and try again.")
                            else:
                                console.print("[bold red]Invalid number. Please choose a number from the table.")
                        except ValueError:
                            console.print("[bold red]Invalid input. Please enter a number.")
                    # If 'n' is selected, exit the loop
                    break
 
            # Continue to the next action prompt
            another_action = Prompt.ask("\n[bold blue]Perform another action? (y/n)", choices=["y", "n"])
            if another_action.lower() != 'y':
                break

# Main execution remains the same
if __name__ == "__main__":
    show_menu()
