import asyncio
from fastapi import APIRouter, HTTPException
from langchain_core.exceptions import OutputParserException
from mysite.chain.auto import reply_chain
from mysite.chain.price import price_chain
from mysite.chain.adres import contact_chain
from mysite.chain.school_chain import topic_chain
from mysite.base_knowledge import KNOWLEDGE
from mysite.database.schema import (
    ReplyInputSchema, ReplyOutSchema,
    TopicInputSchema, TopicOutSchema,
    QuestionInputSchema, QuestionOutSchema,
)


ai_router = APIRouter(prefix='/ai', tags=['AI Assistant'])


@ai_router.post('/topic/', response_model=TopicOutSchema)
async def topic_list(topic: TopicInputSchema):
    text = topic.text.strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес формата берилип жатат')

    try:
        result = await asyncio.wait_for(
            topic_chain.ainvoke({"text": text}), timeout=120
        )
    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модел тапшырманы аткарганы жетишкен жок')

    except OutputParserException:
        raise HTTPException(status_code=500, detail='Моделдин жообу схемага туура келбейт')

    except ValueError:
        raise HTTPException(status_code=500, detail='Жообу толук чыкпай калды')

    return result


@ai_router.post('/reply/', response_model=ReplyOutSchema)
async def reply_list(reply: ReplyInputSchema):
    text = reply.text.strip()
    facts = (reply.facts or KNOWLEDGE).strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес формата берилип жатат')

    try:
        result = await asyncio.wait_for(
            reply_chain.ainvoke({"text": text, "facts": facts}), timeout=120
        )
    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модел тапшырманы аткарганы жетишкен жок')

    except ValueError:
        raise HTTPException(status_code=500, detail='Жообу толук чыкпай калды')

    result = result.strip()

    return ReplyOutSchema(text_draft=result)


@ai_router.post('/price/', response_model=QuestionOutSchema)
async def price_list(question: QuestionInputSchema):
    text = question.text.strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес формата берилип жатат')

    try:
        result = await asyncio.wait_for(
            price_chain.ainvoke({"text": text, "facts": KNOWLEDGE}), timeout=120
        )
    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модел тапшырманы аткарганы жетишкен жок')

    except ValueError:
        raise HTTPException(status_code=500, detail='Жообу толук чыкпай калды')

    result = result.strip()

    return QuestionOutSchema(text_draft=result)


@ai_router.post('/contact/', response_model=QuestionOutSchema)
async def contact_list(question: QuestionInputSchema):
    text = question.text.strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес формата берилип жатат')

    try:
        result = await asyncio.wait_for(
            contact_chain.ainvoke({"text": text, "facts": KNOWLEDGE}), timeout=120
        )
    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модел тапшырманы аткарганы жетишкен жок')

    except ValueError:
        raise HTTPException(status_code=500, detail='Жообу толук чыкпай калды')

    result = result.strip()

    return QuestionOutSchema(text_draft=result)