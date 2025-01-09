from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.traceback import Traceback
import time
import random
from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class StepResult:
    description: str
    status: str = "pending"
    duration: float = 0.0
    error: Optional[str] = None


@dataclass
class TestResult:
    name: str
    steps: List[StepResult]
    status: str = "pending"
    duration: float = 0.0

class TestRunner:
    def __init__(self):
        self.console = Console()
        self.results: List[TestResult] = []
        
    def create_table(self) -> Table:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Status", justify="center", width=10)
        table.add_column("Test Name", justify="left", width=50)
        table.add_column("Progress", justify="left", width=20)
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
            
            # Calculate step progress
            total_steps = len(result.steps)
            completed_steps = sum(1 for step in result.steps if step.status in ["passed", "failed"])
            progress = f"{completed_steps}/{total_steps}"
            
            table.add_row(
                f"[{status_style}]{result.status}[/]",
                result.name,
                progress,
                duration
            )
        
        return table

    def run_tests(self, test_cases: Dict[str, List[str]]):
        # Initialize results with steps
        self.results = [
            TestResult(name=name, steps=[StepResult(description=step) for step in steps])
            for name, steps in test_cases.items()
        ]
        
        failed_tests = []
        
        # Create live display
        with Live(self.create_table(), refresh_per_second=10) as live:
            for result in self.results:
                result.status = "running"
                start_time = time.time()
                
                # Run each step
                for step in result.steps:
                    step.status = "running"
                    live.update(self.create_table())
                    
                    step_start = time.time()
                    success, error = self.execute_step(result.name, step.description)
                    step.duration = time.time() - step_start
                    
                    if success:
                        step.status = "passed"
                    else:
                        step.status = "failed"
                        step.error = error
                        result.status = "failed"
                        failed_tests.append(result)
                        break
                    
                    live.update(self.create_table())
                
                result.duration = time.time() - start_time
                if result.status != "failed":
                    result.status = "passed"
                
                live.update(self.create_table())
        
        # Show summary and failed test details
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "passed")
        failed = len(failed_tests)
        
        self.console.print("\n=== Test Summary ===")
        self.console.print(f"Total: {total} | Passed: [green]{passed}[/] | Failed: [red]{failed}[/]")
        
        if failed_tests:
            self.console.print("\n=== Failed Tests ===")
            for test in failed_tests:
                # Create detailed step report
                steps_text = Text()
                for i, step in enumerate(test.steps, 1):
                    status_color = "green" if step.status == "passed" else "red"
                    steps_text.append(f"\nStep {i}: ", style="bold")
                    steps_text.append(f"{step.description}\n", style=status_color)
                    steps_text.append(f"Status: ", style="bold")
                    steps_text.append(f"{step.status}\n", style=status_color)
                    
                    if step.error:
                        steps_text.append("Error:\n", style="bold red")
                        steps_text.append(f"{step.error}\n", style="red")
                    
                    steps_text.append(f"Duration: {step.duration:.2f}s\n", style="dim")
                    
                    # Stop after the failed step
                    if step.status == "failed":
                        break
                
                panel = Panel(
                    steps_text,
                    title=f"[red]{test.name}[/] (Duration: {test.duration:.2f}s)",
                    border_style="red"
                )
                self.console.print(panel)

    def execute_step(self, test_name: str, step_description: str) -> tuple[bool, Optional[str]]:
        """
        Mock step execution - replace this with actual step execution logic
        Returns (success, error message if failed)
        """
        time.sleep(random.uniform(0.1, 0.3))  # Simulate work
        success = random.choice([True, True, True, False])  # 25% chance of failure
        
        if not success:
            error = f"""Error executing step: {step_description}
Traceback (most recent call last):
  File "test_{test_name}.py", line {random.randint(10, 99)}, in {step_description.lower().replace(' ', '_')}
    assert condition, "Step failed"
AssertionError: Expected condition was not met"""
            return False, error
        
        return True, None

if __name__ == "__main__":
    # Example usage with test steps
    test_cases = {
        "test_user_login": [
            "Initialize test environment",
            "Create test user",
            "Attempt login with credentials",
            "Verify login success",
            "Check session token",
            "Cleanup test data"
        ],
        "test_data_validation": [
            "Setup test database",
            "Insert sample records",
            "Validate data formats",
            "Test boundary conditions",
            "Verify error handling",
            "Remove test records"
        ],
        "test_api_integration": [
            "Start mock API server",
            "Send GET request",
            "Validate response format",
            "Test error scenarios",
            "Check rate limiting",
            "Shutdown mock server"
        ]
    }
    
    runner = TestRunner()
    runner.run_tests(test_cases)
