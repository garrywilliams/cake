from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cake_requests", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cakerequest",
            name="cake_id",
            field=models.IntegerField(db_index=True),
        ),
    ]
