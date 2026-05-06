"""
Singleton LangChain Agent — created once at FastAPI startup, reused for every request.
"""
import logging
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools.calculator_tool import calculator
from tools.document_search_tool import internal_document_search

logger = logging.getLogger(__name__)

_agent_executor: AgentExecutor | None = None


def _build_agent() -> AgentExecutor:
    logger.info("Initialising LangChain singleton agent…")

    llm = ChatOpenAI(model="gpt-4o", temperature=0, streaming=False)

    tools = [calculator, internal_document_search]

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            (
                "You are a helpful AI assistant for the company. "
                "You have access to two tools:\n"
                "1. calculator — for any arithmetic or math questions.\n"
                "2. internal_document_search — for any company-specific questions.\n"
                "Always use a tool when appropriate before answering."
            ),
        ),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)
    logger.info("LangChain singleton agent ready.")
    return executor


def get_agent() -> AgentExecutor:
    """Return the singleton agent, creating it on first call."""
    global _agent_executor
    if _agent_executor is None:
        _agent_executor = _build_agent()
    return _agent_executor


def run_agent(question: str) -> str:
    """Run the singleton agent and return the answer string."""
    executor = get_agent()
    result = executor.invoke({"input": question})
    return result.get("output", "No answer returned.")
