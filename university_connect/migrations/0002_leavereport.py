# Generated by Django 3.0.7 on 2021-11-24 07:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("university_connect", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LeaveReport",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("dates", models.CharField(max_length=255)),
                ("message", models.TextField()),
                ("status", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
