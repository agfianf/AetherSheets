import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph

from integrations.llm import LLMClient
from integrations.scraper import WebScrapper
from prompts.company_research.prompt import (
    ABOUT_AGENT_PROMPT,
    COMPOSER_AGENT_PROMPT,
    FINANCE_AGENT_PROMPT,
    FOUNDER_AGENT_PROMPT,
    NEWS_AGENT_PROMPT,
)

llm = LLMClient()
scrapper = WebScrapper()


class OverallState(TypedDict):
    company: str
    about: Annotated[str, operator.add]
    founder: Annotated[str, operator.add]
    finance: Annotated[str, operator.add]
    news: Annotated[str, operator.add]
    final_summary: str


def about_agent(state: OverallState) -> dict:
    result_search = scrapper.search(
        f"General information about {state['company']}", max_results=5
    )

    input_user = (
        f"Company Name: {state['company']} based on these information:\n{result_search}"
    )
    content = llm.generate(system_prompt=ABOUT_AGENT_PROMPT, input_user=input_user)
    return {"about": content}


def founder_agent(state: OverallState) -> dict:
    result_search = scrapper.search(
        f"Latest Founder and Co-Founder of {state['company']}",
        max_results=5,
    )

    input_user = (
        f"Company Name: {state['company']} based on these information {result_search}"
    )
    content = llm.generate(system_prompt=FOUNDER_AGENT_PROMPT, input_user=input_user)
    return {"founder": content}


def finance_agent(state: OverallState) -> dict:
    result_search = scrapper.search(
        f"Latest financial information of {state['company']}",
        max_results=5,
    )

    input_user = (
        f"Company Name: {state['company']} based on these information {result_search}"
    )
    content = llm.generate(system_prompt=FINANCE_AGENT_PROMPT, input_user=input_user)
    return {"finance": content}


def news_agent(state: OverallState) -> dict:
    result_search = scrapper.search(
        f"Latest News of {state['company']}",
        max_results=5,
    )

    input_user = (
        f"Company Name: {state['company']} based on these information {result_search}"
    )
    content = llm.generate(system_prompt=NEWS_AGENT_PROMPT, input_user=input_user)
    return {"news": content}


def composer_agent(state: OverallState) -> dict:
    # Create the input prompt with all research findings
    input_user = f"""
Company: {state["company"]}

**About Information:**
{state.get("about", "No information available")}

**Founder Information:**
{state.get("founder", "No information available")}

**Financial Information:**
{state.get("finance", "No information available")}

**Recent News:**
{state.get("news", "No information available")}

Please synthesize this information into a comprehensive company summary.
"""

    final_summary = llm.generate(
        system_prompt=COMPOSER_AGENT_PROMPT, input_user=input_user
    )
    return {"final_summary": final_summary}


def create_graph_company_summary():
    graph = StateGraph(state_schema=OverallState)

    graph.add_node("about_agent", about_agent)
    graph.add_node("founder_agent", founder_agent)
    graph.add_node("finance_agent", finance_agent)
    graph.add_node("news_agent", news_agent)
    graph.add_node("composer_agent", composer_agent)

    graph.add_edge(START, "about_agent")
    graph.add_edge(START, "founder_agent")
    graph.add_edge(START, "finance_agent")
    graph.add_edge(START, "news_agent")

    graph.add_edge("about_agent", "composer_agent")
    graph.add_edge("founder_agent", "composer_agent")
    graph.add_edge("finance_agent", "composer_agent")
    graph.add_edge("news_agent", "composer_agent")

    graph.add_edge("composer_agent", END)

    return graph.compile()


if __name__ == "__main__":
    graph = create_graph_company_summary()

    input_state = {"company": "eFishery"}
    result = graph.invoke(input_state)
    print(result)
