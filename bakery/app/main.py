from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud
from .database import SessionLocal
from .schemas import Cake, CakeCreate

description = (
    "This is a fancy Cake Bakery API. You can find all sorts of cakes here!\n\n"
    "Welcome to the Cake Bakery API, a viral sensation in the world of digital bakeries! "
    "This API, crafted with love and a sprinkle of Python magic, allows you to interact "
    "with a virtual bakery's catalog of mouth-watering cakes. Whether you're looking to "
    "browse our extensive cake collection, add a new cake to our showcase, or even remove "
    "a cake from the menu, our API has got you covered.\n\n"
    "More details are available in the README file."
)

app = FastAPI(
    title="Cake Bakery API",
    description=description,
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Garry Williams",
        "url": "http://www.example.com/support",
        "email": "garry.p.williams@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://mit-license.org/",
    },
)

router = APIRouter()


def get_db():
    """
    The function returns a database session and ensures that it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/cakes/",
    tags=["Cakes"],
    response_model=Cake,
    status_code=status.HTTP_201_CREATED,
    summary="Add a cake",
    description="""
        Add a new cake to the bakery. Provide a cake name, comment, 
        a link to a picture of the cake and yum factor between 1 and 5.
        We'll return you the cake you added with its unique ID.
        """,
)
def create_cake(cake: CakeCreate, db: Session = Depends(get_db)):
    return crud.create_cake(db=db, cake_data=cake.model_dump())


@router.get(
    "/cakes/{cake_id}",
    tags=["Cakes"],
    response_model=Cake,
    summary="Retrieve a cake",
    description="Retrieve a cake from the bakery by providing it's unique ID.",
)
def read_cake(cake_id: int, db: Session = Depends(get_db)):
    db_cake = crud.get_cake(db, cake_id=cake_id)
    if db_cake is None:
        raise HTTPException(status_code=404, detail="Cake not found")
    return db_cake


@router.get(
    "/cakes/",
    tags=["Cakes"],
    response_model=List[Cake],
    summary="List all cakes",
    description="""
    Retrieve a list of all cakes in the bakery. 
    You can provide a limit and skip parameter to paginate the results.
    """,
)
def read_cakes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cakes = crud.get_cakes(db, skip=skip, limit=limit)
    return cakes


@router.put(
    "/cakes/{cake_id}",
    tags=["Cakes"],
    response_model=Cake,
    summary="Change a cake",
    description="Change a cake in the bakery by providing it's unique ID and updated data.",
)
def update_cake(cake_id: int, cake: CakeCreate, db: Session = Depends(get_db)):
    updated_cake = crud.update_cake(
        db, cake_id=cake_id, updated_cake_data=cake.model_dump()
    )
    if updated_cake is None:
        raise HTTPException(status_code=404, detail="Cake not found")
    return updated_cake


@router.delete(
    "/cakes/{cake_id}",
    tags=["Cakes"],
    response_model=Cake,
    summary="Remove a cake",
    description="Remove a cake from the bakery by providing it's unique ID.",
)
def delete_cake(cake_id: int, db: Session = Depends(get_db)):
    db_cake = crud.get_cake(db, cake_id=cake_id)
    if db_cake is None:
        raise HTTPException(status_code=404, detail="Cake not found")
    crud.delete_cake(db, cake_id=cake_id)
    return db_cake


app.include_router(router, prefix="/api")
