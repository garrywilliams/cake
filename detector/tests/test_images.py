import io
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from PIL import Image

from app.images import download_image, interpret_output, is_cake, preprocess_image


@patch("requests.get")
def test_download_image(mock_get):
    # Create a simple image and save it to a bytes buffer
    image = Image.new("RGB", (100, 100), color="red")
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)

    # Mock the response
    mock_response = MagicMock()
    mock_response.content = buf.read()
    mock_get.return_value = mock_response

    # Call the function
    image = download_image("http://example.com/image.jpg")

    # Assertions
    assert image is not None
    mock_get.assert_called_with("http://example.com/image.jpg")


def test_preprocess_image():
    # Create a simple image
    original_size = (100, 100)
    target_size = (513, 513)
    image = Image.new("RGB", original_size, color="blue")

    # Call the preprocess function
    processed_image = preprocess_image(image, target_size)

    # Check if the image is resized
    assert processed_image.shape[1:3] == target_size  # Height and width check

    # Check if the image is converted to numpy array and has 3 channels
    assert isinstance(processed_image, np.ndarray)
    assert processed_image.shape[3] == 3  # Channel check

    # Check if the image is uint8
    assert processed_image.dtype == np.uint8

    # Check if a batch dimension is added
    assert processed_image.shape[0] == 1  # Batch dimension check


def test_interpret_output():
    # Create mock output data from a neural network model
    # Simulate a 10x10 image with 21 classes (class IDs 0-20)
    mock_output = np.zeros((1, 10, 10, 21))

    # Set some pixels to 'sweets/desserts' (class ID 20)
    # and some to 'snacks' (class ID 19)
    mock_output[0, :5, :5, 20] = 1  # Top-left quarter is 'sweets/desserts'
    mock_output[0, 5:, 5:, 19] = 1  # Bottom-right quarter is 'snacks'

    # Call the function with a threshold
    threshold = 0.1
    is_cake, proportion_cake_pixels = interpret_output(mock_output, threshold)

    # Check if the function correctly identifies the image as cake
    assert is_cake

    # Check if the proportion is calculated correctly
    # 50% of the image is classified as cake
    assert proportion_cake_pixels == 0.5

    # Test with a higher threshold
    high_threshold = 0.6
    is_cake_high_threshold, _ = interpret_output(mock_output, high_threshold)
    assert not is_cake_high_threshold


@patch("app.images.download_image")
@patch("app.images.preprocess_image")
@patch("tflite_runtime.interpreter.Interpreter")
def test_is_cake(mock_interpreter, mock_preprocess_image, mock_download_image):
    # Mock the download_image function
    mock_image = MagicMock()
    mock_download_image.return_value = mock_image

    # Mock the preprocess_image function
    mock_processed_image = np.random.rand(1, 513, 513, 3).astype(np.uint8)
    mock_preprocess_image.return_value = mock_processed_image

    # Mock the TensorFlow Lite interpreter
    mock_interpreter_instance = MagicMock()
    mock_interpreter.return_value = mock_interpreter_instance

    # Mock the output of the model
    mock_output_data = np.random.rand(1, 10, 10, 21)  # Adjust dimensions as needed
    mock_interpreter_instance.get_tensor.return_value = mock_output_data

    # Call the is_cake function
    url = "http://example.com/image.jpg"
    model_path = "path/to/model.tflite"
    threshold = 0.1
    is_cake_result, proportion = is_cake(url, model_path, threshold)

    # Assertions
    assert isinstance(is_cake_result, bool)
    assert 0 <= proportion <= 1
    mock_download_image.assert_called_with(url)
    mock_preprocess_image.assert_called_with(mock_image)
    mock_interpreter.assert_called_with(model_path=model_path)
    mock_interpreter_instance.allocate_tensors.assert_called()
    mock_interpreter_instance.set_tensor.assert_called()
    mock_interpreter_instance.invoke.assert_called()
    mock_interpreter_instance.get_tensor.assert_called()
