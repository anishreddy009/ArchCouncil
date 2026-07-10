from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage,HumanMessage

load_dotenv()

llm_cost = ChatGroq(model = "llama-3.1-8b-instant")
llm_performance = ChatGroq(model= "meta-llama/llama-4-scout-17b-16e-instruct")
llm_security = ChatGroq(model = 'openai/gpt-oss-120b',reasoning_effort='low')
llm_maintainability = ChatGroq(model = 'qwen/qwen3-32b' , reasoning_effort="none",max_tokens=200)

question = "Should we use PostgreSQL or MongoDB for a new order-tracking service?"

llm_performance_responce = llm_performance.invoke([SystemMessage(content = "You are an advocate of an architecture council. Argue for whatever maximizes speed and scalability, with specific reasoning under 10 words"),
                                                   HumanMessage(content=question),])
llm__cost_responce = llm_cost.invoke([SystemMessage(content = "You are an advocate of an architecture council. Argue for whatever minimizes the cost for building the infrastructure, with specific reasoning under 10 words"),
                                      HumanMessage(content=question),])
llm_security_responce = llm_security.invoke([SystemMessage(content="You are the Security advocate on a SOFTWARE architecture council reviewing technical decisions for an engineering team. Argue for whatever minimizes attack surface, data exposure risk, and compliance burden. You must commit to ONE clear recommendation. Do not say 'it depends' or weigh both sides equally — pick a position and defend it. Be specific about real threat models. Under 10 words."),
                                             HumanMessage(content=question)])
llm_maintainability_response = llm_maintainability.invoke([SystemMessage(content= "You are the Maintainability advocate on a SOFTWARE architecture council reviewing technical decisions for an engineering team. Argue for whatever is easiest for a small team to understand, debug, and evolve over the next few years. You must commit to ONE clear recommendation. Do not say 'it depends' or weigh both sides equally — pick a position and defend it. Be specific about real operational scenarios. Under 10 words."),
                                                          HumanMessage(content=question)])

print("=== PERFORMANCE ===")
print("#performance "+ llm_performance_responce.content)

print("=== COST ===")
print("#cost " + llm__cost_responce.content)


print("=== SECURITY ===")
print(llm_security_responce.content)
print()
print("=== MAINTAINABILITY ===")
print(llm_maintainability_response.content)