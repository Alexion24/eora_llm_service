from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.gigachat_client import query_gigachat

app = FastAPI(
    title="EORA LLM Service",
    description=(
        "Сервис для ответов на вопросы клиентов компании EORA по решениям "
        "для ритейлеров с использованием OpenAI GPT-3.5/4 через асинхронный клиент."
    ),
    version="1.0.0",
)


class Question(BaseModel):
    question: str = Field(
        ...,
        example="Что вы можете сделать для ритейлеров?",
        description="Текст вопроса клиента к сервису.",
    )


class AnswerResponse(BaseModel):
    answer: str = Field(
        ...,
        example="EORA предлагает решения для ритейлеров с помощью ИИ: чат-боты для HR, визуальный поиск товаров по фото и автоматизация контакт-центров.",
    )
    sources: Optional[List[str]] = Field(
        None,
        example=[
            "https://eora.ru/cases/chat-boty/hr-bot-dlya-magnit-kotoriy-priglashaet-na-sobesedovanie",
            "https://eora.ru/cases/kazanexpress-poisk-tovarov-po-foto",
        ],
        description="Список ссылок на кейсы, использованные для формирования ответа.",
    )


@app.post(
    "/answer",
    response_model=AnswerResponse,
    summary="Получить ответ на вопрос клиента",
    description=(
        "Принимает вопрос клиента и возвращает информативный ответ, "
        "который ссылается на проекты и кейсы компании EORA. \n\n"
        "Если вопрос связан с ритейлерами, то предоставляются ключевые ссылки для удобства."
    ),
)
async def answer_question(q: Question):
    try:
        answer = await query_gigachat(q.question)
        sources = []
        if "ритейлер" in q.question.lower():
            sources = [
                "https://eora.ru/cases/chat-boty/hr-bot-dlya-magnit-kotoriy-priglashaet-na-sobesedovanie",
                "https://eora.ru/cases/kazanexpress-poisk-tovarov-po-foto",
            ]
        return AnswerResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
