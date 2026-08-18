import streamlit as st

from graph.workflow import build_graph


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
)


# --------------------------------------------------
# Initialize LangGraph
# --------------------------------------------------

@st.cache_resource
def get_graph():
    return build_graph()


graph = get_graph()


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.title("Enterprise Knowledge Assistant")

    st.markdown(
        """
        ### Capabilities

        📚**Knowledge Search**  
        Ask questions about company knowledge.

        🎫**Support Tickets**  
        Create support tickets through MCP.

        🛡️**Guardrails**  
        Protect sensitive information.

        📊**RAGAS Evaluation**  
        Evaluate RAG response quality.
        """
    )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# Main header
# --------------------------------------------------

st.title("🤖 Enterprise Knowledge Assistant")

st.caption(
    "AI-powered enterprise assistant using "
    "LangGraph + RAG + RAGAS + Guardrails + MCP"
)


# --------------------------------------------------
# Display previous messages
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # Display additional information for assistant
        if message["role"] == "assistant":

            if message.get("evaluation_scores"):

                with st.expander("📊 RAGAS Evaluation"):

                    scores = message["evaluation_scores"]

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Faithfulness",
                            f"{scores.get('faithfulness', 0):.2f}",
                        )

                    with col2:
                        st.metric(
                            "Answer Relevancy",
                            f"{scores.get('answer_relevancy', 0):.2f}",
                        )

                    if message.get("evaluation_summary"):
                        st.caption(
                            message["evaluation_summary"]
                        )

            if message.get("mcp_result"):

                mcp_result = message["mcp_result"]

                with st.expander("🎫 Ticket Information"):

                    if mcp_result.get("success"):

                        col1, col2 = st.columns(2)

                        with col1:
                            st.write(
                                "**Ticket ID:**",
                                mcp_result.get(
                                    "ticket_id",
                                    "N/A",
                                ),
                            )

                            st.write(
                                "**Title:**",
                                mcp_result.get(
                                    "title",
                                    "N/A",
                                ),
                            )

                        with col2:
                            st.write(
                                "**Priority:**",
                                mcp_result.get(
                                    "priority",
                                    "N/A",
                                ).capitalize(),
                            )

                            st.write(
                                "**Status:**",
                                mcp_result.get(
                                    "status",
                                    "N/A",
                                ).capitalize(),
                            )

                    else:

                        st.error(
                            mcp_result.get(
                                "error",
                                "Ticket operation failed.",
                            )
                        )


# --------------------------------------------------
# Chat input
# --------------------------------------------------

question = st.chat_input(
    "Ask a question or request an action..."
)


if question:

    # --------------------------------------------------
    # Display user message
    # --------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # --------------------------------------------------
    # Execute LangGraph
    # --------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            initial_state = {
                "question": question,
                "retrieved_documents": [],
                "answer": "",
                "evaluation_scores": {},
                "evaluation_summary": "",
                "mcp_action": "",
                "mcp_result": {},
            }

            try:

                result = graph.invoke(
                    initial_state
                )

                answer = result.get(
                    "answer",
                    "I could not generate a response.",
                )

                evaluation_scores = result.get(
                    "evaluation_scores",
                    {},
                )

                evaluation_summary = result.get(
                    "evaluation_summary",
                    "",
                )

                mcp_result = result.get(
                    "mcp_result",
                    {},
                )

                # --------------------------------------------------
                # Display final answer
                # --------------------------------------------------

                st.markdown(answer)

                # --------------------------------------------------
                # RAGAS results
                # --------------------------------------------------

                if evaluation_scores:

                    with st.expander(
                        "📊 RAGAS Evaluation"
                    ):

                        col1, col2 = st.columns(2)

                        with col1:

                            st.metric(
                                "Faithfulness",
                                f"{evaluation_scores.get('faithfulness', 0):.2f}",
                            )

                        with col2:

                            st.metric(
                                "Answer Relevancy",
                                f"{evaluation_scores.get('answer_relevancy', 0):.2f}",
                            )

                        if evaluation_summary:

                            st.caption(
                                evaluation_summary
                            )

                # --------------------------------------------------
                # MCP results
                # --------------------------------------------------

                if mcp_result:

                    with st.expander(
                        "🎫 Ticket Information"
                    ):

                        if mcp_result.get("success"):

                            col1, col2 = st.columns(2)

                            with col1:

                                st.write(
                                    "**Ticket ID:**",
                                    mcp_result.get(
                                        "ticket_id",
                                        "N/A",
                                    ),
                                )

                                st.write(
                                    "**Title:**",
                                    mcp_result.get(
                                        "title",
                                        "N/A",
                                    ),
                                )

                            with col2:

                                st.write(
                                    "**Priority:**",
                                    mcp_result.get(
                                        "priority",
                                        "N/A",
                                    ).capitalize(),
                                )

                                st.write(
                                    "**Status:**",
                                    mcp_result.get(
                                        "status",
                                        "N/A",
                                    ).capitalize(),
                                )

                        else:

                            st.error(
                                mcp_result.get(
                                    "error",
                                    "Ticket operation failed.",
                                )
                            )

                # --------------------------------------------------
                # Store assistant message
                # --------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "evaluation_scores": evaluation_scores,
                        "evaluation_summary": evaluation_summary,
                        "mcp_result": mcp_result,
                    }
                )

            except Exception as exc:

                error_message = (
                    "I encountered an error while "
                    "processing your request."
                )

                st.error(error_message)

                st.exception(exc)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )