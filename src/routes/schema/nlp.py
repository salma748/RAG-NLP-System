

from pydantic import BaseModel, Field
"""
class PushDataRequest(BaseModel):
    do_reset: int = 0
   """


class SearchRequest(BaseModel):
    text: str = Field(min_length=1)
    top_k: int = Field(default=5, gt=0, le=20)



