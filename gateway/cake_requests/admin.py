import requests
from django.contrib import admin
from django.utils.html import format_html

from .models import CakeRequest

# from gateway.settings import CAKE_URL


@admin.register(CakeRequest)
class CakeRequestAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "image_thumbnail",
        "image_url",
        "is_cake",
        "proportion",
        "tolerance",
        "access_count",
        "timestamp",
        "status",
    )

    # To display a thumbnail of the picture, define a custom method
    def image_thumbnail(self, obj):
        if obj.image_url:
            return format_html(
                f'<a href="{obj.image_url}" target="_blank"><img src="{obj.image_url}" width="50" height="50" /></a>'
            )
        return ""

    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = "Image Thumbnail"

    def proportion_display(self, obj):
        return f"{obj.proportion}"

    proportion_display.admin_order_field = "proportion"  # Allows column order sorting
    proportion_display.short_description = "Proportion"  # Column header

    def tolerance_display(self, obj):
        return f"{obj.tolerance}"

    tolerance_display.admin_order_field = "tolerance"  # Allows column order sorting
    tolerance_display.short_description = "Tolerance"  # Column header

    # Optionally, you can use list_filter and search_fields for filtering and searching
    list_filter = ("is_cake", "status")
    search_fields = ("cake_id", "image_url", "proportion")

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        cake_details = None

        if object_id:
            cake_request = CakeRequest.objects.get(pk=object_id)
            if cake_request.status == "A" and cake_request.cake_id > 0:
                try:
                    response = requests.get(
                        f"http://localhost:8080/api/cakes/{cake_request.cake_id}"
                    )
                    if response.status_code == 200:
                        cake_details = response.json()
                except requests.RequestException:
                    cake_details = {"error": "Error fetching details"}

        # TODO: Cake details are available for a custom template

        extra_context["cake_details"] = cake_details
        return super().changeform_view(request, object_id, form_url, extra_context)
