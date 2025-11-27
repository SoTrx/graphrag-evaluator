"""Conditional Workflow for Content Review with Azure AI Foundry Agents"""

import asyncio
import os
from dataclasses import dataclass

from azure.identity.aio import AzureCliCredential
from azure.ai.projects.aio import AIProjectClient

from agent_framework import (
    AgentExecutor,
    AgentExecutorRequest,
    AgentExecutorResponse,
    ChatMessage,
    Role,
    WorkflowBuilder,
    WorkflowContext,
    executor,
)

from evangelist_agent import agent as evangelist_agent, EvangelistAgent
from contentreview_agent import agent as reviewer_agent, ReviewAgent
from publisher_agent import agent as publisher_agent

# Module-level storage for lazy initialization
_credential = None
_client = None
_workflow = None
_initialized = False


@dataclass
class ReviewResult:
    """Data class to hold review results"""
    review_result: str
    reason: str
    draft_content: str


@executor(id="to_evangelist_content_result")
async def to_evangelist_content_result(
    response: AgentExecutorResponse, 
    ctx: WorkflowContext[AgentExecutorRequest]
) -> None:
    """Convert evangelist agent response to structured format and forward to reviewer"""
    print(f"📝 [Workflow] Raw response from evangelist agent: {response.agent_run_response}")
    agent = EvangelistAgent.model_validate_json(response.agent_run_response.text)
    user_msg = ChatMessage(Role.USER, text=agent.draft_content)
    await ctx.send_message(AgentExecutorRequest(messages=[user_msg], should_respond=True))


@executor(id="to_reviewer_result")
async def to_reviewer_result(
    response: AgentExecutorResponse, 
    ctx: WorkflowContext[ReviewResult]
) -> None:
    """Convert reviewer agent response to structured format"""
    print(f"🔍 [Workflow] Raw response from reviewer agent: {response.agent_run_response.text}")
    
    parsed = ReviewAgent.model_validate_json(response.agent_run_response.text)
    await ctx.send_message(
        ReviewResult(
            review_result=parsed.review_result,
            reason=parsed.reason,
            draft_content=parsed.draft_content,
        )
    )


def select_targets(review: ReviewResult, target_ids: list[str]) -> list[str]:
    """
    Select workflow path based on review result
    
    Args:
        review: The review result containing decision
        target_ids: List of [handle_review_id, save_draft_id]
    
    Returns:
        List containing the selected target executor ID
    """
    handle_review_id, save_draft_id = target_ids
    if review.review_result == "Yes":
        print(f"✅ [Workflow] Review passed - routing to save_draft")
        return [save_draft_id]
    else:
        print(f"❌ [Workflow] Review failed - routing to handle_review")
        return [handle_review_id]


@executor(id="handle_review")
async def handle_review(review: ReviewResult, ctx: WorkflowContext[str]) -> None:
    """Handle review failures"""
    if review.review_result == "No":
        message = f"Review failed: {review.reason}, please revise the draft."
        print(f"⚠️ [Workflow] {message}")
        await ctx.yield_output(message)
    else:
        await ctx.send_message(
            AgentExecutorRequest(
                messages=[ChatMessage(Role.USER, text=review.draft_content)], 
                should_respond=True
            )
        )


@executor(id="save_draft")
async def save_draft(review: ReviewResult, ctx: WorkflowContext[AgentExecutorRequest]) -> None:
    """Save draft content by sending to publisher agent"""
    # Only called for approved drafts by selection_func
    await ctx.send_message(
        AgentExecutorRequest(
            messages=[ChatMessage(Role.USER, text=review.draft_content)], 
            should_respond=True
        )
    )





    
# Create agent executors
evangelist_executor = AgentExecutor(evangelist_agent, id="evangelist_agent")
reviewer_executor = AgentExecutor(reviewer_agent, id="reviewer_agent")
publisher_executor = AgentExecutor(publisher_agent, id="publisher_agent")
    
    # Build the conditional workflow
workflow = (
        WorkflowBuilder()
        .set_start_executor(evangelist_executor)
        .add_edge(evangelist_executor, to_evangelist_content_result)
        .add_edge(to_evangelist_content_result, reviewer_executor)
        .add_edge(reviewer_executor, to_reviewer_result)
        .add_multi_selection_edge_group(
            to_reviewer_result,
            [handle_review, save_draft],
            selection_func=select_targets,
        )
        .add_edge(save_draft, publisher_executor)
        .build()
    )


# Create the lazy workflow wrapper instance - this is what gets imported
# workflow = _workflow

