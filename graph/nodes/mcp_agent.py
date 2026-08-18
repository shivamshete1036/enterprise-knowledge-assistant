import asyncio

from graph.state import GraphState
from mcp_client.ticket_client import create_ticket


def extract_ticket_title(question: str) -> str:
    """
    Generate a meaningful ticket title from the user's request.
    """

    question_lower = question.lower()

    if "vpn" in question_lower:
        return "VPN connection issue"

    if "password" in question_lower:
        return "Password issue"

    if "login" in question_lower:
        return "Login issue"

    if "email" in question_lower:
        return "Email issue"

    if "network" in question_lower:
        return "Network issue"

    if "laptop" in question_lower:
        return "Laptop issue"

    return "Enterprise support request"


def mcp_agent(state: GraphState) -> GraphState:
    """
    Handle requests that require interaction with the
    external enterprise ticket system through MCP.
    """

    print("\n[MCP Agent] Starting...")

    question = state["question"]
    question_lower = question.lower()

    # --------------------------------------------------
    # Detect ticket request
    # --------------------------------------------------

    ticket_keywords = [
        "create a ticket",
        "create ticket",
        "raise a ticket",
        "raise ticket",
        "open a ticket",
        "open ticket",
        "report an issue",
        "report issue",
        "it ticket",
        "support ticket",
    ]

    should_create_ticket = any(
        keyword in question_lower
        for keyword in ticket_keywords
    )

    if not should_create_ticket:
        print("[MCP Agent] No ticket request detected.")

        return {
            **state,
            "mcp_action": "none",
            "mcp_result": {},
        }

    print("[MCP Agent] Ticket request detected.")

    # --------------------------------------------------
    # Detect priority
    # --------------------------------------------------

    priority = "medium"

    if "critical" in question_lower:
        priority = "critical"

    elif (
        "high priority" in question_lower
        or "high-priority" in question_lower
        or (
            "high" in question_lower
            and "priority" in question_lower
        )
    ):
        priority = "high"

    elif (
        "low priority" in question_lower
        or "low-priority" in question_lower
        or (
            "low" in question_lower
            and "priority" in question_lower
        )
    ):
        priority = "low"

    print(
        f"[MCP Agent] Detected priority: {priority}"
    )

    # --------------------------------------------------
    # Generate ticket title
    # --------------------------------------------------

    title = extract_ticket_title(question)

    print(
        f"[MCP Agent] Ticket title: {title}"
    )

    # --------------------------------------------------
    # Call MCP create_ticket tool
    # --------------------------------------------------

    print(
        "[MCP Agent] Calling MCP create_ticket tool..."
    )

    result = asyncio.run(
        create_ticket(
            title=title,
            description=question,
            priority=priority,
        )
    )

    # --------------------------------------------------
    # Extract structured MCP response
    # --------------------------------------------------

    structured_content = getattr(
        result,
        "structuredContent",
        None,
    )

    if structured_content is None:
        structured_content = {}

    print(
        "[MCP Agent] Ticket created:",
        structured_content,
    )

    # --------------------------------------------------
    # Create clean user-facing response
    # --------------------------------------------------

    if structured_content.get("success"):

        ticket_id = structured_content.get(
            "ticket_id",
            "Unknown",
        )

        ticket_title = structured_content.get(
            "title",
            title,
        )

        ticket_priority = structured_content.get(
            "priority",
            priority,
        )

        ticket_status = structured_content.get(
            "status",
            "open",
        )

        answer = (
            "I've created a support ticket for you.\n\n"
            f"**Ticket ID:** {ticket_id}\n"
            f"**Title:** {ticket_title}\n"
            f"**Priority:** {ticket_priority.capitalize()}\n"
            f"**Status:** {ticket_status.capitalize()}"
        )

    else:

        error_message = structured_content.get(
            "error",
            "Unknown MCP error.",
        )

        answer = (
            "I couldn't create the support ticket.\n\n"
            f"**Reason:** {error_message}"
        )

    # --------------------------------------------------
    # Return updated state
    # --------------------------------------------------

    return {
        **state,
        "answer": answer,
        "mcp_action": "create_ticket",
        "mcp_result": structured_content,
    }