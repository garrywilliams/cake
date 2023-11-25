from io import BytesIO
from unittest.mock import patch

import numpy as np
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app  # Ensure this import points to your FastAPI app instance

client = TestClient(app)


def test_detect_cake_success():
    # Create a dummy image and convert it to BytesIO
    dummy_image = Image.fromarray(
        np.uint8(np.random.rand(100, 100, 3) * 255)
    )  # 10x10 random image
    img_byte_arr = BytesIO()
    dummy_image.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)  # Reset the buffer to the beginning after writing

    with patch("app.main.is_cake", return_value=(True, 0.75)) as mock_is_cake:
        response = client.post(
            "/detect-cake/",
            json={"url": "http://example.com/image.jpg", "threshold": 0.1},
        )

        assert response.status_code == 200
        assert response.json() == {"is_cake": True, "proportion": 0.75}
