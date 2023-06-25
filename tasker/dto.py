from pydantic import BaseModel, Field


class Task(BaseModel):
    title: str = Field(min_length=2, max_length=90)
    is_complete: bool = Field(default=False)
    primary: bool = Field(default=False)

