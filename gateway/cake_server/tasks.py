import requests
from celery import shared_task

from cake_requests.models import CakeRequest


@shared_task
def make_external_api_call(method, url, data=None, params=None, headers=None):
    response = requests.request(method, url, json=data, params=params, headers=headers)
    return create_response_dict(response)


def create_response_dict(response):
    return {
        "status_code": response.status_code,
        "content": response.json()
        if response.headers.get("content-type") == "application/json"
        else response.text,
        "headers": dict(response.headers),
    }


@shared_task
def create_cake_request(cake_id, image_url, detector_threshold, detector_response):
    content = detector_response.get("content", {})
    proportion = content.get("proportion", 0.0)
    is_cake = content.get("is_cake", False)

    # Create a new CakeRequest instance
    cake_request = CakeRequest(
        cake_id=cake_id,
        image_url=image_url,
        is_cake=is_cake,
        proportion=proportion,
        tolerance=detector_threshold,
        access_count=0,
        status="A",
    )

    cake_request.save()


# Add a task that get a given CakeRequest and increment its access_count by 1
@shared_task
def increment_cake_request_access_count(cake_id):
    try:
        cake_request = CakeRequest.objects.filter(cake_id=cake_id).first()
        if cake_request:
            cake_request.access_count += 1
            cake_request.save()
        else:
            pass
    except CakeRequest.DoesNotExist:
        pass


# Add a task that get a given CakeRequest and set its status to 'D'
@shared_task
def delete_cake_request(cake_id):
    try:
        cake_request = CakeRequest.objects.filter(cake_id=cake_id).first()
        if cake_request:
            cake_request.status = "D"
            cake_request.save()
        else:
            pass
    except CakeRequest.DoesNotExist:
        pass
