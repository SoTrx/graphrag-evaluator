# 🔄 Import Workflow and Agent Framework Components
# Core components for building sophisticated agent workflows

import base64
import json
import os  # 🔧 Environment variable access
from typing import Any, List

from agent_framework import (  # 🏗️ Workflow orchestration tools
    ChatAgent,
    ChatMessage,
    ConcurrentBuilder,
    DataContent,
    Role,
    TextContent,
    WorkflowBuilder,
    WorkflowEvent,
    WorkflowOutputEvent,
    WorkflowViz,
)
from agent_framework.azure import AzureAIAgentClient, AzureOpenAIChatClient
from agent_framework.openai import (
    OpenAIChatClient,  # 🤖 GitHub Models client integration
)
from azure.ai.projects.aio import AIProjectClient
from azure.identity import AzureCliCredential, DefaultAzureCredential
from dotenv import load_dotenv
from IPython.display import HTML, SVG, display
from pydantic import BaseModel

# Helper Functions for Workflow Visualization


def print_workflow_viz(workflow, title="Workflow Visualization"):
    """
    Display workflow visualization in multiple formats (Mermaid, DiGraph, SVG).

    Args:
        workflow: The workflow object to visualize
        title: Optional title for the visualization output
    """
    print(f"\n{'=' * 80}")
    print(f"🎨 {title}")
    print('=' * 80)

    viz = WorkflowViz(workflow)

    # Print Mermaid format
    print("\n📊 Mermaid Diagram:")
    print('-' * 80)
    print(viz.to_mermaid())
    print('-' * 80)

    # Print DiGraph format
    print("\n🔗 DiGraph:")
    print('-' * 80)
    print(viz.to_digraph())
    print('-' * 80)

    # Export and display SVG
    svg_file = viz.export(format="svg")
    print(f"\n💾 SVG exported to: {svg_file}")

    # Display the SVG
    display_svg(svg_file)

    return svg_file


def display_svg(svg_file):
    """
    Display an SVG file in the notebook with fallback rendering.

    Args:
        svg_file: Path to the SVG file
    """
    print(f"\n🖼️ Displaying SVG: {svg_file}")

    if not svg_file or not os.path.exists(svg_file):
        print("❌ SVG file not found.")
        return

    try:
        # Try direct SVG rendering
        display(SVG(filename=svg_file))
    except Exception as e:
        print(f"⚠️ Direct SVG render failed: {e}")
        print("Attempting HTML fallback...")
        try:
            # Fallback to HTML rendering
            with open(svg_file, "r", encoding="utf-8") as f:
                svg_text = f.read()
            display(HTML(svg_text))
            print("✅ SVG displayed via HTML fallback")
        except Exception as inner:
            print(f"❌ HTML fallback also failed: {inner}")


def print_workflow_event(event, index=None):
    """
    Print workflow event with formatted output based on event type.

    Args:
        event: The workflow event to display
        index: Optional index number for the event
    """

    # Header with index if provided
    header = f"\n{'=' * 80}\n"
    if index is not None:
        header += f"📋 Event #{index}\n"
    else:
        header += f"📋 Workflow Event\n"
    header += f"{'=' * 80}"
    print(header)

    # Check if this is a WorkflowOutputEvent (special handling)
    if isinstance(event, WorkflowOutputEvent):
        print(f"🎯 Event Type: WorkflowOutputEvent")

        if event.source_executor_id:
            print(f"   🤖 Executor: {event.source_executor_id}")

        if hasattr(event, 'data') and event.data:
            print(f"   📦 Output Data:")
            print(f"   {'-' * 76}")

            # Handle different data types
            if isinstance(event.data, str):
                # String data - try to parse as JSON
                try:
                    parsed_data = json.loads(event.data)
                    print(f"   {json.dumps(parsed_data, indent=6)}")
                except (json.JSONDecodeError, TypeError):
                    # Not JSON, print as-is
                    print(f"   {event.data}")
            elif isinstance(event.data, BaseModel):
                # Pydantic model - use model_dump_json
                print(f"   {event.data.model_dump_json(indent=6)}")
            elif hasattr(event.data, '__dict__'):
                # Object with __dict__ - try to serialize
                try:
                    print(
                        f"   {json.dumps(event.data.__dict__, indent=6, default=str)}")
                except Exception:
                    print(f"   {event.data}")
            else:
                # Default: just print the data
                print(f"   {event.data}")
    else:
        # Standard WorkflowEvent
        print(f"⚙️  Event Type: {type(event).__name__}")

        if event.executor_id:
            print(f"   🤖 Executor ID: {event.executor_id}")

        if event.origin:
            print(f"   📍 Source: {event.origin}")

        if hasattr(event, 'data') and event.data is not None:
            # Check if data has a text attribute
            if hasattr(event.data, 'text'):
                content = event.data.text
                print(f"   💬 Content:")
                print(f"   {'-' * 76}")
                # Indent the content for better readability
                for line in content.split('\n'):
                    print(f"   {line}")
            else:
                print(f"   📦 Data: {event.data}")
        else:
            print(f"   ⚠️  No data available")

    print(f"{'=' * 80}")
