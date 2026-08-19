from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Message sent by the user"
    )