import io

import numpy as np
import requests
import tflite_runtime.interpreter as tflite
from fastapi import HTTPException
from PIL import Image


def download_image(url):
    """
    The function `download_image` takes a URL as input, downloads the image from that URL, and returns
    the image object.

    :param url: The URL of the image you want to download
    :return: an image object.
    """
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    return image


def preprocess_image(image, target_size=(513, 513)):
    """
    The function preprocesses an image by resizing it to a target size, converting it to a numpy array,
    ensuring it is a 3-channel RGB image, converting it to uint8 data type, and adding a batch
    dimension.

    :param image: The input image that needs to be preprocessed. It can be either a PIL image or a numpy
    array
    :param target_size: The target_size parameter is a tuple that specifies the desired size of the
    image after resizing. In this case, the default target size is (513, 513), which means the image
    will be resized to have a width of 513 pixels and a height of 513 pixels
    :return: a preprocessed image.
    """
    # Resize the image to the target size
    image = image.resize(target_size)

    # Convert the image to a numpy array
    image = np.array(image)

    # Ensure it's a 3-channel RGB image
    if image.ndim == 2:
        image = np.stack((image,) * 3, axis=-1)
    elif image.shape[2] > 3:
        image = image[:, :, :3]

    # Ensure the image is uint8
    image = image.astype(np.uint8)

    # Add a batch dimension
    image = np.expand_dims(image, axis=0)
    return image


# Function to interpret the model's output and check for cake (sweets/desserts or snacks)
def interpret_output(output_data, threshold=0.1):
    """
    The function `interpret_output` takes in the output data from a neural network model and calculates
    the proportion of pixels classified as either 'sweets/desserts' or 'snacks', and determines if this
    proportion exceeds a given threshold.

    :param output_data: The output_data parameter is the raw output from a neural network model. It is
    expected to be a multi-dimensional array, typically with shape (batch_size, height, width,
    num_classes), where batch_size is the number of images in the batch, height and width are the
    dimensions of each image,
    :param threshold: The threshold parameter is a value between 0 and 1 that determines the minimum
    proportion of cake pixels required for the function to classify the image as containing cake. If the
    proportion of cake pixels exceeds the threshold, the function will return True for the is_cake
    variable
    :return: The function `interpret_output` returns a tuple containing two values: `is_cake` and
    `proportion_cake_pixels`.
    """
    # Convert the raw output to a numpy array (if it's not already)
    output_array = np.array(output_data)

    # Remove the batch dimension
    output_array = np.squeeze(output_array)

    # Find the class with the highest probability for each pixel
    class_map = np.argmax(output_array, axis=-1)

    # IDs for 'sweets/desserts' and 'snacks'
    sweets_desserts_id = 20
    snacks_id = 19

    # Count how many pixels are classified as 'sweets/desserts' or 'snacks'
    sweets_desserts_pixels = np.sum(class_map == sweets_desserts_id)
    snacks_pixels = np.sum(class_map == snacks_id)

    # Calculate the total number of pixels classified as either 'sweets/desserts' or 'snacks'
    total_cake_pixels = sweets_desserts_pixels + snacks_pixels

    # Total number of pixels in the image
    total_pixels = class_map.size

    # Calculate the proportion of cake pixels
    proportion_cake_pixels = total_cake_pixels / total_pixels

    # Check if the proportion of cake pixels exceeds the threshold
    is_cake = proportion_cake_pixels > threshold
    return is_cake, proportion_cake_pixels  # Return both the result and the proportion


# Function to classify image
def is_cake(
    url, model_path, threshold=0.1
):  # You can change the default threshold here
    """
    The `is_cake` function takes in a URL of an image, a model path for a TFLite model, and an optional
    threshold value, and returns whether the image contains a cake or not, along with the proportion of
    confidence.

    :param url: The URL of the image you want to classify as a cake or not
    :param model_path: The `model_path` parameter is the path to the TFLite model file that you want to
    use for cake detection. This file should have the extension `.tflite` and contain the trained model
    that can classify images as cake or not cake
    :param threshold: The threshold parameter is used to determine the minimum confidence level required
    for an image to be classified as a cake. If the proportion of the cake class in the output tensor is
    above the threshold, the image will be classified as a cake. You can adjust the threshold value to
    make the classification more or less
    :return: a tuple containing two values: a boolean indicating whether the image is classified as a
    cake or not, and a proportion value indicating the confidence level of the classification.
    """
    try:
        image = download_image(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error downloading image: {e}")

    processed_image = preprocess_image(image)

    # Load TFLite model and allocate tensors
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Set the input tensor
    interpreter.set_tensor(input_details[0]["index"], processed_image)

    # Run the model
    interpreter.invoke()

    # Get the output tensor
    output_data = interpreter.get_tensor(output_details[0]["index"])

    # Interpret results with the custom threshold
    is_cake_result, proportion = interpret_output(output_data, threshold)
    return bool(is_cake_result), proportion
