"""Pretty printing utilities for console output."""
from typing import Union

from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class PrettyConsole:
    """Utility class for pretty printing context and evaluation results."""

    def __init__(self):
        """Initialize the pretty console with a Rich Console instance."""
        self.console = Console()

    def print_context(
        self, title: str, context_response: Union[str, dict, list], context_obj=None
    ):
        """Pretty print context response with colors and formatting.

        Args:
            title: The title to display in the panel
            context_response: The context response (string, dict, or list)
            context_obj: Optional context object to display metadata from
        """
        self.console.print()

        # Display the main response
        if isinstance(context_response, (dict, list)):
            # For structured data, show it as formatted JSON
            self.console.print(
                Panel(
                    JSON.from_data(context_response),
                    title=f"[bold green]📄 {title} - Response[/bold green]",
                    border_style="blue",
                    expand=False,
                )
            )
        else:
            # For string responses, show as text
            self.console.print(
                Panel(
                    Text(str(context_response), style="bright_blue"),
                    title=f"[bold green]📄 {title} - Response[/bold green]",
                    border_style="blue",
                    expand=False,
                )
            )

        # If we have the full context object, show additional details
        if context_obj is not None:
            self.console.print()

            # Create a table for context metadata
            metadata_table = Table(
                title=f"[bold cyan]📋 {title} - Context Metadata[/bold cyan]",
                show_header=True,
                header_style="bold magenta",
            )
            metadata_table.add_column(
                "Property", style="yellow", justify="left")
            metadata_table.add_column(
                "Value", style="bright_green", justify="left")

            # Show available attributes of the context object
            for attr_name in dir(context_obj):
                if not attr_name.startswith("_"):  # Skip private attributes
                    try:
                        attr_value = getattr(context_obj, attr_name)
                        if not callable(attr_value):  # Skip methods
                            # Truncate long values for display
                            str_value = str(attr_value)
                            if len(str_value) > 100:
                                str_value = str_value[:97] + "..."
                            metadata_table.add_row(attr_name, str_value)
                    except Exception:
                        metadata_table.add_row(
                            attr_name, "[red]Error accessing value[/red]"
                        )

            self.console.print(metadata_table)

    def print_evaluation_result(self, title: str, result: dict):
        """Pretty print evaluation result with colors and formatting.

        Args:
            title: The title to display for the evaluation results
            result: The evaluation result dictionary
        """
        self.console.print()

        # Create a table for the evaluation metrics
        table = Table(
            title=f"[bold cyan]📊 {title}[/bold cyan]",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Metric", style="yellow", justify="left")
        table.add_column("Score", style="bright_green", justify="center")
        table.add_column("Reason", style="white", justify="left")

        # Add rows for each metric in the result
        for key, value in result.items():
            if isinstance(value, dict):
                score = value.get("score", "N/A")
                reason = value.get("reason", "No reason provided")
                table.add_row(
                    key,
                    str(score),
                    reason[:50] + "..." if len(reason) > 50 else reason,
                )
            else:
                table.add_row(key, str(value), "")

        self.console.print(table)

        # Also show the full JSON for detailed inspection
        self.console.print()
        self.console.print(
            Panel(
                JSON.from_data(result),
                title="[bold yellow]📋 Detailed Result JSON[/bold yellow]",
                border_style="yellow",
                expand=False,
            )
        )

    def print(self, *args, **kwargs):
        """Wrapper for console.print to allow direct printing.

        Args:
            *args: Arguments to pass to console.print
            **kwargs: Keyword arguments to pass to console.print
        """
        self.console.print(*args, **kwargs)
