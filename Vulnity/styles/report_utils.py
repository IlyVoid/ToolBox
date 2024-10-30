# styling/report_utils.py

from datetime import datetime

def generate_report(url, results):
    report = f"Vulnerability Assessment Report for {url}\n"
    report += "=" * 80 + "\n"
    report += f"Report Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "=" * 80 + "\n"
    
    for test, vulnerabilities in results.items():
        report += f"\nTest: {test}\n"
        report += "-" * 80 + "\n"
        if vulnerabilities:
            for v in vulnerabilities:
                status = "Vulnerable" if v['vulnerable'] else "Secure"
                report += f"  - Payload: {v['payload']}\n"
                report += f"    Status: {status}\n"
                report += f"    Reason: {v['reason']}\n"
        else:
            report += "  - No vulnerabilities found.\n"
    
    report += "=" * 80 + "\n"
    report += "End of Report\n"
    
    return report
