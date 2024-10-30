# styling/console_utils.py

from rich.console import Console
from rich.table import Table

console = Console()

def display_results(results):
    result_table = Table(title="Vulnerability Test Results")
    result_table.add_column("Vulnerability", style="cyan")
    result_table.add_column("Status", justify="center")

    for test, vulnerabilities in results.items():
        if any(v['vulnerable'] for v in vulnerabilities):
            status = "[red]Vulnerable[/red]"
        else:
            status = "[green]Secure[/green]"
        result_table.add_row(test, status)

    console.print(result_table)
