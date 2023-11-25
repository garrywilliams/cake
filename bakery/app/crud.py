from sqlalchemy.orm import Session

from .models import Cake


def create_cake(db: Session, cake_data: dict) -> Cake:
    cake = Cake(**cake_data)
    db.add(cake)
    db.commit()
    db.refresh(cake)
    return cake


def get_cake(db: Session, cake_id: int):
    return db.query(Cake).filter(Cake.id == cake_id).first()


def get_cakes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cake).offset(skip).limit(limit).all()


def update_cake(db: Session, cake_id: int, updated_cake_data: dict):
    db_cake = db.query(Cake).filter(Cake.id == cake_id).first()
    if db_cake is None:
        return None  # or raise an exception, depending on your design choice
    for key, value in updated_cake_data.items():
        setattr(db_cake, key, value)
    db.commit()
    return db_cake


def delete_cake(db: Session, cake_id: int):
    db_cake = db.query(Cake).filter(Cake.id == cake_id).first()
    db.delete(db_cake)
    db.commit()
