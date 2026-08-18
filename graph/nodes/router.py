from graph.state import GraphState


def request_router(state: GraphState) -> str:
    """
    Route the user's request to either the RAG pipeline
    or the MCP action pipeline.

    Returns:
        "knowledge" -> RAG pipeline
        "action"    -> MCP pipeline
    """

    question = state["question"].lower().strip()

    # --------------------------------------------------
    # Action / MCP request detection
    # --------------------------------------------------

    action_keywords = [
        "create a ticket",
        "create ticket",
        "raise a ticket",
        "raise ticket",
        "open a ticket",
        "open ticket",
        "support ticket",
        "it ticket",
        "report an issue",
        "report issue",
    ]

    if any(
        keyword in question
        for keyword in action_keywords
    ):
        print("[Router] Request classified as: ACTION")

        return "action"

    # --------------------------------------------------
    # Default route
    # --------------------------------------------------

    print("[Router] Request classified as: KNOWLEDGE")

    return "knowledge"