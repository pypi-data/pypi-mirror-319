from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.columns import Columns
import time
import random
from dataclasses import dataclass
from typing import List, Optional, Dict
from statistics import mean, median, stdev
from collections import Counter

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


    def generate_statistics(self) -> Panel:
        # Collect duration statistics
        test_durations = [r.duration for r in self.results]
        step_durations = [step.duration for r in self.results for step in r.steps]
        
        # Status statistics
        test_statuses = Counter(r.status for r in self.results)
        step_statuses = Counter(step.status for r in self.results for step in r.steps)
        
        # Calculate step statistics
        steps_per_test = [len(r.steps) for r in self.results]
        
        # Create statistics tables
        duration_table = Table(show_header=True, title="Duration Statistics", title_style="bold cyan")
        duration_table.add_column("Metric", style="bold")
        duration_table.add_column("Tests", justify="right")
        duration_table.add_column("Steps", justify="right")
        
        def format_duration(d: float) -> str:
            return f"{d:.2f}s"
        
        duration_table.add_row(
            "Average",
            format_duration(mean(test_durations)),
            format_duration(mean(step_durations))
        )
        duration_table.add_row(
            "Median",
            format_duration(median(test_durations)),
            format_duration(median(step_durations))
        )
        if len(test_durations) > 1:
            duration_table.add_row(
                "Std Dev",
                format_duration(stdev(test_durations)),
                format_duration(stdev(step_durations))
            )
        duration_table.add_row(
            "Min",
            format_duration(min(test_durations)),
            format_duration(min(step_durations))
        )
        duration_table.add_row(
            "Max",
            format_duration(max(test_durations)),
            format_duration(max(step_durations))
        )
        duration_table.add_row(
            "Total",
            format_duration(sum(test_durations)),
            format_duration(sum(step_durations))
        )

        # Status breakdown table
        status_table = Table(show_header=True, title="Status Breakdown", title_style="bold cyan")
        status_table.add_column("Status", style="bold")
        status_table.add_column("Tests", justify="right")
        status_table.add_column("Steps", justify="right")
        
        for status in ['passed', 'failed', 'skipped']:
            status_table.add_row(
                status.capitalize(),
                str(test_statuses.get(status, 0)),
                str(step_statuses.get(status, 0))
            )

        # Test composition table
        composition_table = Table(show_header=True, title="Test Composition", title_style="bold cyan")
        composition_table.add_column("Metric", style="bold")
        composition_table.add_column("Value", justify="right")
        
        composition_table.add_row("Total Tests", str(len(self.results)))
        composition_table.add_row("Total Steps", str(sum(steps_per_test)))
        composition_table.add_row("Avg Steps/Test", f"{mean(steps_per_test):.1f}")
        composition_table.add_row("Min Steps/Test", str(min(steps_per_test)))
        composition_table.add_row("Max Steps/Test", str(max(steps_per_test)))

        # Calculate pass rate
        pass_rate_table = Table(show_header=True, title="Pass Rates", title_style="bold cyan")
        pass_rate_table.add_column("Metric", style="bold")
        pass_rate_table.add_column("Rate", justify="right")
        
        test_pass_rate = (test_statuses.get('passed', 0) / len(self.results)) * 100
        total_steps = sum(step_statuses.values())
        step_pass_rate = (step_statuses.get('passed', 0) / total_steps) * 100
        
        pass_rate_table.add_row("Test Pass Rate", f"{test_pass_rate:.1f}%")
        pass_rate_table.add_row("Step Pass Rate", f"{step_pass_rate:.1f}%")

        # Arrange tables in a grid
        grid = Columns([
            Panel(duration_table, title="Time Analysis"),
            Panel(status_table, title="Status Analysis")
        ])
        grid2 = Columns([
            Panel(composition_table, title="Composition Analysis"),
            Panel(pass_rate_table, title="Success Rates")
        ])

        return Panel(
            Text.assemble(
                grid, "\n", grid2,
                justify="center"
            ),
            title="Test Execution Statistics",
            border_style="cyan"
        )

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
        
        # Show statistics
        self.console.print("\n=== Test Statistics ===")
        self.console.print(self.generate_statistics())
        
        # Show failed test details
        if failed_tests:
            self.console.print("\n=== Failed Tests ===")
            for test in failed_tests:
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
