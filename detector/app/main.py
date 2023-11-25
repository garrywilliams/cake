from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .images import is_cake

description = """
This API is designed to detect cakes in images. Upload an image URL,
and it will return whether there is a cake in the image and the
proportion of the image that is cake.
"""

app = FastAPI(
    title="Cake Image Detector API",
    description=description,
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Garry Williams",
        "url": "http://contact.url",
        "email": "garry.p.williams@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)


# Pydantic model for the query parameters
class CakeQuery(BaseModel):
    url: str = Field(
        ...,
        title="Image URL",
        description="The URL of the image to analyze for cake presence.",
        json_schema_extra={"example": "http://example.com/image.jpg"},
    )
    threshold: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        title="Detection Threshold",
        description="""
            The threshold for detecting cake in the image,
            ranging from 0.0 (no confidence) to 1.0 (full confidence).
            """,
        json_schema_extra={"example": 0.1},
    )


# Pydantic model for the response object
class CakeResponse(BaseModel):
    is_cake: bool = Field(
        ..., description="Whether the image is classified as containing a cake."
    )
    proportion: float = Field(
        ..., description="The proportion of the image classified as cake."
    )


@app.post("/detect-cake/", tags=["Cakes"], response_model=CakeResponse)
async def detect_cake(query: CakeQuery):
    """
    Detect whether an image contains a cake.

    This endpoint takes a URL of an image and a threshold value for detection.
    It processes the image using a machine learning model to determine if the image contains a cake
    and what proportion of the image is cake.

    - **url**: The URL of the image to detect cake in.
    - **threshold**: The confidence threshold to classify an image as containing a cake.
    """
    try:
        is_cake_result, proportion = is_cake(query.url, "1.tflite", query.threshold)
        return CakeResponse(is_cake=is_cake_result, proportion=proportion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")
