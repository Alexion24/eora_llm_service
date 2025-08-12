from gigachat import GigaChatAsyncClient
from gigachat.models import ChatCompletion
from app.config import settings

client = GigaChatAsyncClient(
    credentials=settings.giga_chat_key,
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    verify_ssl_certs=False,
)


async def query_gigachat(prompt: str) -> str:
    system_prompt = (
        "Ты — ассистент компании EORA. Отвечай по вопросам, "
        "используя данные по проектам EORA для ритейлеров."
    )
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
    }

    completion: ChatCompletion = await client.achat(payload)
    answer = completion.choices[0].message.content
    return answer
