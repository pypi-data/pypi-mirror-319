from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.traceback import Traceback
import time
import random  # Just for demo purposes
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TestResult:
    name: str
    status: str = "pending"
    trace: Optional[str] = None
    duration: float = 0.0


class TestRunner:
    def __init__(self):
        self.console = Console()
        self.results: List[TestResult] = []
        
    def create_table(self) -> Table:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Status", justify="center", width=10)
        table.add_column("Test Name", justify="left", width=50)
        table.add_column("Duration", justify="right", width=10)
        
        status_colors = {
            "pending": "white",
            "running": "yellow",
            "passed": "green",
            "failed": "red",
            "skipped": "blue"
        }
        
        for result in self.results:
            status_style = f"{status_colors[result.status]}"
            duration = f"{result.duration:.2f}s" if result.duration else ""
            table.add_row(
                f"[{status_style}]{result.status}[/]",
                result.name,
                duration
            )
        
        return table

    def run_tests(self, test_names: List[str]):
        # Initialize results
        self.results = [TestResult(name=name) for name in test_names]
        
        failed_tests = []
        
        # Create live display
        with Live(self.create_table(), refresh_per_second=10) as live:
            for result in self.results:
                result.status = "running"
                live.update(self.create_table())
                
                # Simulate test execution
                start_time = time.time()
                success, trace = self.execute_test(result.name)  # This is where actual test would run
                result.duration = time.time() - start_time
                
                if success:
                    result.status = "passed"
                else:
                    result.status = "failed"
                    result.trace = trace
                    failed_tests.append(result)
                    
                live.update(self.create_table())
        
        # Show summary and failed test details
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "passed")
        failed = sum(1 for r in self.results if r.status == "failed")
        
        self.console.print("\n=== Test Summary ===")
        self.console.print(f"Total: {total} | Passed: [green]{passed}[/] | Failed: [red]{failed}[/]")
        
        if failed_tests:
            self.console.print("\n=== Failed Tests ===")
            for test in failed_tests:
                panel = Panel(
                    f"{test.trace}",
                    title=f"[red]{test.name}[/]",
                    border_style="red"
                )
                self.console.print(panel)

    def execute_test(self, test_name: str) -> tuple[bool, Optional[str]]:
        """
        Mock test execution - replace this with actual test running logic
        Returns (success, trace if failed)
        """
        time.sleep(random.uniform(0.1, 0.5))  # Simulate work
        success = random.choice([True, True, False])  # 33% chance of failure
        
        if not success:
            trace = f"""Traceback (most recent call last):
  File "test_{test_name}.py", line 42, in {test_name}
    assert expected == actual
AssertionError: Expected 'foo' but got 'bar'"""
            return False, trace
        
        return True, None

if __name__ == "__main__":
    # Example usage
    test_names = [
        "test_user_login",
        "test_user_logout",
        "test_data_validation",
        "test_error_handling",
        "test_api_response",
        "test_database_connection"
    ]
    
    runner = TestRunner()
    runner.run_tests(test_names)
