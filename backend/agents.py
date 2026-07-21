from typing import TypedDict, Union,Any
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from config import models,chair_model,councilPrompt,chairmanPrompt
from dotenv import load_dotenv

load_dotenv()

llms = {
    name:init_chat_model(
        model_provider='groq',
        temperature =0.8,
        max_tokens=200,
        **config_dict
    )
    for name,config_dict in models.items()
}

council = {
    name : create_agent(
        model=llm,
        system_prompt=councilPrompt
    )
    for name,llm in llms.items()
}

chair_llm = init_chat_model(model = chair_model,temperature = 0.8,model_provider='groq')
chairman = create_agent(chair_llm,system_prompt=chairmanPrompt)
