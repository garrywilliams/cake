from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

from .database import Base


class Cake(Base):
    __tablename__ = "cakes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), index=True, nullable=False)
    comment = Column(String(200), nullable=False)
    imageUrl = Column(String, nullable=False)
    yumFactor = Column(Integer, nullable=False)

    @validates("name")
    def validate_name(self, key, value):
        if len(value) > 30:
            raise ValueError("The name field must not exceed 30 characters")
        if len(value) < 5:
            raise ValueError("The name field must not be fewer than 5 characters")
        return value

    @validates("comment")
    def validate_comment(self, key, value):
        if len(value) > 200:
            raise ValueError("The comment field must not exceed 200 characters")
        if len(value) < 5:
            raise ValueError("The comment field must not be fewer than 5 characters")
        return value

    @validates("yumFactor")
    def validate_yumFactor(self, key, value):
        if not 1 <= value <= 5:
            raise ValueError("yumFactor must be between 1 and 5")
        return value
