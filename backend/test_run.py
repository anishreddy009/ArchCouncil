from orchestrator import run_council
import asyncio

result = asyncio.run(run_council("who is the best football player of all time?"))

# for name,response in result['agent_responses'].items():
#     print(f'{name}\n\n{response}\n')


print("chairman")
print(result['chairman_response'])