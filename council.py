from dotenv import load_dotenv
from pydantic import BaseModel, Field

from typing import Annotated, Union, List
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

class LLM_Response_Structured_Output(BaseModel):
    message: str = Field(description="The assistant's full text response to the user's message.")

messages_history = Annotated[List[Union[SystemMessage, HumanMessage, AIMessage]], "The message history of the conversation."]
models = {
    'guard_rail_agent': init_chat_model(model="llama-3.3-70b-versatile", model_provider="groq", streaming=True).with_structured_output(LLM_Response_Structured_Output),
    'llm_1': init_chat_model(model="llama-3.1-8b-instant", model_provider="groq", streaming=True).with_structured_output(LLM_Response_Structured_Output),
    'llm_2': init_chat_model(model="llama-3.3-70b-versatile", model_provider="groq", streaming=True).with_structured_output(LLM_Response_Structured_Output),
    'llm_3': init_chat_model(model="meta-llama/llama-4-scout-17b-16e-instruct", model_provider="groq", streaming=True).with_structured_output(LLM_Response_Structured_Output),
    'llm_4': init_chat_model(model="openai/gpt-oss-120b", model_provider="groq", streaming=True).with_structured_output(LLM_Response_Structured_Output),
}


system_message = SystemMessage(content="You are a helpful assistant that can explain things to a 5 year old. Response should be just 1 sentence.")
message_history = [system_message]
judge_system_message = SystemMessage(content="You are a llm responses ranker. You will be given 4 responses from different llms along with the chat history. You will rank them based on their quality, relevance, and helpfulness. You should return only the best response from the 4 responses. You should not return any of the other responses. You should not return any explanations or reasoning. You should only return the best response.")
judge_message_history = [judge_system_message]

while True:
    input_text = input("You: ")
    message_history.append(HumanMessage(content=input_text))
    judge_message_history.append(HumanMessage(content=input_text))

    responses = {}

    for model_name, model in models.items():
        if model_name == 'guard_rail_agent':
            continue
        try:
            response = model.invoke(message_history)
            responses[model_name] = response
            print(f"{model_name}: {response.message}")
        except Exception as e:
            print(f"{model_name}: [failed to respond: {e}]")

    if not responses:
        print("All models failed to respond. Skipping this turn.")
        continue

    aggregated_responses = HumanMessage(
        content="The responses for the above question and chat are:" +
        "\n".join([f"model_{i}_response: {response.message}" for i, response in enumerate(responses.values())])
    )

    final_response = models['guard_rail_agent'].invoke(judge_message_history + [aggregated_responses])
    print(f"Final Response: {final_response.message}")

    final_ai_message = AIMessage(content=final_response.message)
    message_history.append(final_ai_message)
    judge_message_history.append(final_ai_message)