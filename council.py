from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage,HumanMessage

load_dotenv()

llm_cost = init_chat_model(model = "groq:llama-3.1-8b-instant",temperature=0.8, streaming=True)
llm_performance = init_chat_model(model= "groq:meta-llama/llama-4-scout-17b-16e-instruct",temperature=0.8, streaming=True)
llm_security = init_chat_model(model = 'groq:openai/gpt-oss-120b',reasoning_effort='low',temperature=0.8, streaming=True)
llm_maintainability = init_chat_model(model = 'groq:qwen/qwen3-32b' , reasoning_effort="none",max_tokens=200,temperature=0.8, streaming=True)

question = "Should we use PostgreSQL or MongoDB for a new order-tracking service?"

print("=== PERFORMANCE ===")
for chunk in llm_performance.stream([SystemMessage(content = "You are an advocate of an architecture council. Argue for whatever maximizes speed and scalability, with specific reasoning under 10 words"),
                                                   HumanMessage(content=question),]):
    print(chunk.content,end='')

print('\n')
print("=== COST ===")
for chunk in llm_cost.stream([SystemMessage(content = "You are an advocate of an architecture council. Argue for whatever minimizes the cost for building the infrastructure, with specific reasoning under 10 words"),
                                      HumanMessage(content=question),]):
    print(chunk.content,end='')

print('\n')
print("=== SECURITY ===")
for chunk in llm_security.stream([SystemMessage(content="You are the Security advocate on a SOFTWARE architecture council reviewing technical decisions for an engineering team. Argue for whatever minimizes attack surface, data exposure risk, and compliance burden. You must commit to ONE clear recommendation. Do not say 'it depends' or weigh both sides equally — pick a position and defend it. Be specific about real threat models. Under 10 words."),
                                             HumanMessage(content=question)]):
    print(chunk.content,end='')

print('\n')
print("=== MAINTAINABILITY ===")

for chunk in llm_maintainability.stream([SystemMessage(content= "You are the Maintainability advocate on a SOFTWARE architecture council reviewing technical decisions for an engineering team. Argue for whatever is easiest for a small team to understand, debug, and evolve over the next few years. You must commit to ONE clear recommendation. Do not say 'it depends' or weigh both sides equally — pick a position and defend it. Be specific about real operational scenarios. Under 10 words."),
                                                          HumanMessage(content=question)]):
    print(chunk.content,end='')
    