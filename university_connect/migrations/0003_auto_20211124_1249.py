# Generated by Django 3.0.7 on 2021-11-24 07:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("university_connect", "0002_leavereport"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leavereport",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
