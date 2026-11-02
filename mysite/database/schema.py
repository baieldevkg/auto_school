from pydantic import BaseModel, Field


class TopicInputSchema(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class TopicOutSchema(BaseModel):
    topic: str


class ReplyInputSchema(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    facts: str | None = Field(default=None, max_length=1000)


class ReplyOutSchema(BaseModel):
    text_draft: str


class QuestionInputSchema(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class QuestionOutSchema(BaseModel):
    text_draft: str