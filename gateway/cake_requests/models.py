from django.db import models


class CakeRequest(models.Model):
    id = models.AutoField(primary_key=True)
    cake_id = models.IntegerField(db_index=True)
    image_url = models.URLField()
    is_cake = models.BooleanField()
    proportion = models.FloatField()
    tolerance = models.FloatField()
    access_count = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, default="A")  # 'Active' or 'Deleted'

    def __str__(self):
        return (
            f"{self.id} [🍰 {self.cake_id}]" if self.cake_id > 0 else f"{self.id} [No 🍰]"
        )
