from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CakeRequest",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("cake_id", models.IntegerField()),
                ("image_url", models.URLField()),
                ("is_cake", models.BooleanField()),
                ("proportion", models.FloatField()),
                ("tolerance", models.FloatField()),
                ("access_count", models.PositiveIntegerField(default=0)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(default="A", max_length=1)),
            ],
        ),
    ]
