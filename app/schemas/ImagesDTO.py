from datetime import datetime

from pydantic import BaseModel


class ImageOut(BaseModel):
    id: int
    title: str
    url: str
    alt: str
    upload_date: datetime

    class Config:
        from_attributes = True