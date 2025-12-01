from typing import List
from pydantic import BaseModel

class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[dict]
