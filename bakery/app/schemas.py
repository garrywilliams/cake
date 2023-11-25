from pydantic import BaseModel, Field


class CakeBase(BaseModel):
    name: str = Field(..., max_length=30)
    comment: str = Field(..., max_length=200)
    imageUrl: str = Field(
        default="http://example.com/default_cake.jpg", pattern="^http[s]?://.+"
    )
    yumFactor: int = Field(..., gt=0, le=5)


class CakeCreate(CakeBase):
    pass


class Cake(CakeBase):
    id: int

    class ConfigDict:
        from_attributes = True
