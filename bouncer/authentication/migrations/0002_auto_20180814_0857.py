# Generated by Django 2.1 on 2018-08-14 08:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuthToken",
            fields=[
                (
                    "key",
                    models.CharField(
                        max_length=32,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Key",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "user",
                    models.ManyToManyField(
                        related_name="auth_token",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "UserToken",
                "verbose_name_plural": "UserTokens",
                "permissions": (("can_view_email_entry", "Can view email entries"),),
            },
        ),
        migrations.RemoveField(model_name="usertoken", name="user"),
        migrations.DeleteModel(name="UserToken"),
    ]
