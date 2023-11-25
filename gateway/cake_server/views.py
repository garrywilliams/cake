# cake_server/views.py
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from gateway.settings import CAKE_URL, DETECTOR_THRESHOLD, DETECTOR_URL

from .serializers import CakeSerializer
from .tasks import (
    create_cake_request,
    delete_cake_request,
    increment_cake_request_access_count,
    make_external_api_call,
)


class CakeDetectorMixin:
    def _handle_detector_service(self, image_url):
        detector_data = {"url": image_url, "threshold": DETECTOR_THRESHOLD}
        detector_response = make_external_api_call.delay(
            "POST", DETECTOR_URL, data=detector_data
        ).get()

        if detector_response["status_code"] != 200:
            return {
                "error": "Invalid cake image. Please try again with a different image."
            }

        if not detector_response.get("content", {}).get("is_cake", False):
            create_cake_request.delay(
                cake_id=0,
                image_url=image_url,
                detector_threshold=DETECTOR_THRESHOLD,
                detector_response=detector_response,
            )
            return {
                "error": "Couldn't see the cake. Please try again with a different image."
            }

        return detector_response

    def _create_cake(self, data, image_url, detector_response):
        cake_response = make_external_api_call.delay("POST", CAKE_URL, data=data).get()

        if cake_response["status_code"] != 201:
            return {"error": "We couldn't add your cake. Please try again."}

        create_cake_request.delay(
            cake_id=cake_response.get("content").get("id"),
            image_url=image_url,
            detector_threshold=DETECTOR_THRESHOLD,
            detector_response=detector_response,
        )

        return {
            "data": cake_response["content"],
            "status": cake_response["status_code"],
        }

    def _update_cake(self, cake_id, data):
        cake_response = make_external_api_call.delay(
            "PUT", f"{CAKE_URL}{cake_id}/", data=data
        ).get()

        if cake_response["status_code"] != 200:
            return Response(
                {"error": "Could not update the cake. Please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data=cake_response["content"],
            status=cake_response["status_code"],
            content_type="application/json",
        )


class CakeListView(CakeDetectorMixin, APIView):
    """
    get:
    Retrieve a list of cakes.

    post:
    Create a new cake.
    """

    @swagger_auto_schema(
        responses={200: CakeSerializer(many=True)},
        operation_summary="List all cakes.",
        operation_description="""
        Retrieve a list of all cakes in the bakery. You can provide a limit and skip parameter to paginate the results.
        """,
        manual_parameters=[
            openapi.Parameter(
                "skip",
                openapi.IN_QUERY,
                description="Number of items to skip",
                type=openapi.TYPE_INTEGER,
                default=0,
            ),
            openapi.Parameter(
                "limit",
                openapi.IN_QUERY,
                description="Maximum number of items to return",
                type=openapi.TYPE_INTEGER,
                default=10,
            ),
        ],
    )
    def get(self, request, format=None):
        # Forward GET request to external service
        skip = request.query_params.get("skip", 0)
        limit = request.query_params.get("limit", 10)
        task = make_external_api_call.delay(
            "GET", CAKE_URL, params={"skip": skip, "limit": limit}
        )
        response = task.get()
        status_code = response["status_code"]
        return Response(
            data=response["content"],
            status=status_code,
        )

    @swagger_auto_schema(
        request_body=CakeSerializer,
        responses={201: CakeSerializer},
        operation_summary="Add a cake.",
        operation_description="""
        Add a new cake to the bakery. Provide a cake name, comment,
        a link to a picture of the cake and yum factor between 1 and 5.
        We'll return you the cake you added with its unique ID.
        """,
    )
    def post(self, request, format=None):
        data = request.data
        image_url = data.get("imageUrl")

        if not image_url:
            return Response(
                {"error": "Please provide an imageUrl."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        detector_response = self._handle_detector_service(image_url)
        if detector_response.get("error"):
            return Response(detector_response, status=status.HTTP_400_BAD_REQUEST)

        cake_response = self._create_cake(data, image_url, detector_response)
        if cake_response.get("error"):
            return Response(cake_response, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            cake_response["data"],
            status=cake_response["status"],
            content_type="application/json",
        )


class CakeDetailView(CakeDetectorMixin, APIView):
    """
    get:
    Retrieve a specific cake by its ID.

    put:
    Update a specific cake by its ID.

    delete:
    Delete a specific cake by its ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve a cake.",
        operation_description="Retrieve a cake from the bakery by providing it's unique ID.",
        responses={200: CakeSerializer()},
    )
    def get(self, request, cake_id, format=None):
        # Forward GET request for a specific cake to external service
        task = make_external_api_call.delay("GET", f"{CAKE_URL}{cake_id}/")
        cake_response = task.get()
        response = Response(
            data=cake_response[
                "content"
            ],  # Assuming 'content' contains the response content
            status=cake_response["status_code"],
            headers=cake_response["headers"],
            content_type="application/json",
        )

        # if there's a cake_response with an id then delete the cake_request
        if cake_response.get("content").get("id"):
            increment_cake_request_access_count.delay(cake_id=cake_id)

        return response

    @swagger_auto_schema(
        request_body=CakeSerializer,
        responses={200: CakeSerializer(), 422: "HTTPValidationError"},
        operation_summary="Change a cake.",
        operation_description="Change a cake in the bakery by providing it's unique ID and updated data.",
        manual_parameters=[
            openapi.Parameter(
                "cake_id",
                openapi.IN_PATH,
                description="ID of the Cake to update",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
    )
    def put(self, request, cake_id, format=None):
        serializer = CakeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        image_url = request.data.get("imageUrl")
        if image_url:
            detector_response = self._handle_detector_service(image_url)
            if detector_response.get("error"):
                return Response(detector_response, status=status.HTTP_400_BAD_REQUEST)

        return self._update_cake(cake_id, request.data)

    @swagger_auto_schema(
        operation_summary="Remove a cake.",
        operation_description="Remove a cake from the bakery by providing it's unique ID.",
        responses={200: "Cake deleted successfully"},
    )
    def delete(self, request, cake_id, format=None):
        # Forward DELETE request for a specific cake to external service
        task = make_external_api_call.delay("DELETE", f"{CAKE_URL}{cake_id}/")
        cake_response = task.get()
        response = Response(
            data=cake_response[
                "content"
            ],  # Assuming 'content' contains the response content
            status=cake_response["status_code"],
            headers=cake_response["headers"],
            content_type="application/json",
        )
        # if there's a cake_response with an id then delete the cake_request
        if cake_response.get("content").get("id"):
            delete_cake_request.delay(cake_id=cake_id)

        return response
