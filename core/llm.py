from openai import AsyncOpenAI
from .config import get_settings

settings = get_settings()
client = AsyncOpenAI(api_key=settings.openai_api_key)

async def chat(messages: list[dict], tools: list[dict] | None = None):
    response = await client.chat.completions.create(
        model=settings.model,
        messages=messages,
        tools=tools or []
    )
    return response.choices[0].message

