from django.db import migrations


def create_superuser(apps, schema_editor):
    User = apps.get_model("auth", "User")

    # Check if a user with the specified username or email already exists
    if (
        not User.objects.filter(username="admin").exists()
        and not User.objects.filter(email="admin@example.com").exists()
    ):
        admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password1"
        )
        admin.is_active = True
        admin.is_admin = True
        admin.save()


class Migration(migrations.Migration):
    dependencies = [
        ("cake_requests", "0002_alter_cakerequest_cake_id"),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
