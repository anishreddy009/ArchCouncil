import asyncio
import random 
from agents import chairman,council
from langchain_core.messages import HumanMessage

async def invoking_agent(agent,user_input:str) -> str:
    result = await agent.ainvoke({"messages":[HumanMessage(content=user_input)]})
    return result['messages'][-1].content

async def collect_responses(user_input : str) -> dict[str:str]:
    tasks = [invoking_agent(agent,user_input) for agent in council.values()]
    result = await asyncio.gather(*tasks)
    response = [i for i in result if i is not None]
    return dict(zip(council.keys(),response))

async def run_chairman(user_input:str,council_response=dict[str:str]) ->str:
    responses = list(council_response.values())
    random.shuffle(responses)
    labeled = "\n\n".join(f"Response {chr(65 + i)}: {r}" for i, r in enumerate(responses))
    chairman_input = f"user_question: {user_input}+ {labeled}"

    chairman_response = await chairman.ainvoke({"messages":[HumanMessage(content = chairman_input)]})
    return chairman_response['messages'][-1].content

async def run_council(user_input: str) -> dict:
    council_responses = await collect_responses(user_input)
    chairman_answer = await run_chairman(user_input, council_responses)

    return {
        "question": user_input,
        "agent_responses": council_responses,
        "chairman_response": chairman_answer,
    }