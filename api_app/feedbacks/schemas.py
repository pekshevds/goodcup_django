from datetime import datetime

from pydantic import BaseModel, Field


class FeedbackParam(BaseModel):
    wb_nmId_list: list[int] = Field(default_factory=list)
    ya_offerId_list: list[str] = Field(default_factory=list)


class Feedback(BaseModel):
    user_name: str = ""
    feedback: str = ""
    date: datetime = Field(default=datetime.now())
    valuation: int = 0


class Feedbacks(BaseModel):
    feedbacks: list[Feedback] = Field()
