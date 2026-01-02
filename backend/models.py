from pydantic import BaseModel

class Resource(BaseModel):
    id: int
    subject: str
    name: str            # renamed from topic
    resource_type: str
    link: str

    avg_rating: float = 0.0
    rating_count: int = 0
