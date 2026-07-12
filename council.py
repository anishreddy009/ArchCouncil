#import

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Annotated, Union, List , Any
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import asyncio

load_dotenv()

class UserInput(BaseModel):
    message : str = Field(description="User query")

class CouncilInput(BaseModel):
    messages : List[Union[AIMessage,HumanMessage,SystemMessage]]


class Response(BaseModel):
    message : str = Field(description="Output of llm ")

models = {
    'llm1': {"model": "llama-3.1-8b-instant"},
    'llm_2': {"model": "llama-3.3-70b-versatile"},
    'llm_3': {"model": "meta-llama/llama-4-scout-17b-16e-instruct"},
    'llm_4': {"model": "openai/gpt-oss-20b", "reasoning_effort": "low"},
}

chair_model = 'openai/gpt-oss-120b'


councilPrompt = "You are one member of a council of AI advisors answering the user's question. Give your own honest, direct, complete answer based on your own reasoning — don't hedge, don't try to guess what other advisors might say, and don't present both sides equally if you actually have a view. Be specific and back up your reasoning with concrete points, not vague generalities. If there's a genuine important caveat, mention it briefly, but still commit to a clear answer."

chairmanPrompt ='''You are the Chairman of a council of AI advisors. You have been given the user's original question along with independent answers from four council members. Your job is to synthesize these into ONE final, clear answer for the user — you are not just picking your favorite response or averaging them.

Read all four answers carefully. Then:
1. Identify where the council genuinely agrees — that consensus is a strong signal and should anchor your answer.
2. Identify the strongest distinct point each member raised that the others missed or underweighted, and fold in whatever is genuinely valuable.
3. If members meaningfully disagree, don't paper over it — briefly note the disagreement and use your own judgment to decide which position is better reasoned, explaining why.
4. Do not simply copy one member's answer verbatim. Produce a single, well-reasoned, original synthesis.
5. Be direct and commit to a clear final answer. Do not hedge or say "it depends" if the council's reasoning actually points somewhere specific.

Format your response as: a short final answer/recommendation first, followed by a brief explanation of your reasoning (2-4 sentences), and — only if relevant — one line noting any significant disagreement among the council and why you resolved it the way you did.'''


llms = {
    name: init_chat_model(
        model_provider="groq",
        temperature=0.8,
        max_tokens=400,
        **config,
    )
    for name, config in models.items()
}

agents = {name : create_agent(model=model_name, system_prompt= councilPrompt)
          for name,model_name in llms.items()}

chair_llm = init_chat_model(model=chair_model, model_provider = 'groq',temperature = 1.2)

chair_agent = create_agent(model=chair_llm,system_prompt= chairmanPrompt)
# print(agents)

async def invoking_agent(agent, user_input):
    return await agent.ainvoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        }
    )
    
async def collect_responses(user_input:str,agents) -> dict[str:Any]:

    tasks = [invoking_agent(agent,user_input) for agent in agents.values()]
    responses = await asyncio.gather(*tasks)
    
    return {model : response["messages"][-1].content for model,response in zip(agents.keys(),responses)}

temp = asyncio.run(collect_responses(input("provide your question: "),agents))

for llm,ai in temp.items():
    print(llm,ai)
    print()
