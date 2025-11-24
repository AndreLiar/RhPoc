from typing import List
from openai import OpenAI
from ..config import get_settings

_settings = get_settings()

# Use standard OpenAI API
_client = OpenAI(api_key=_settings.OPENAI_API_KEY)


def get_openai_client() -> OpenAI:
    return _client


def create_chat_completion(system_prompt: str, messages: List[dict], max_tokens: int = 800) -> str:
    client = get_openai_client()
    resp = client.chat.completions.create(
        model=_settings.OPENAI_CHAT_MODEL,
        max_tokens=max_tokens,
        temperature=0.2,
        messages=[{"role": "system", "content": system_prompt}, *messages],
    )
    return resp.choices[0].message.content


def create_embeddings(texts: List[str]) -> List[List[float]]:
    client = get_openai_client()
    resp = client.embeddings.create(
        model=_settings.OPENAI_EMBEDDING_MODEL,
        input=texts,
    )
    return [d.embedding for d in resp.data]
