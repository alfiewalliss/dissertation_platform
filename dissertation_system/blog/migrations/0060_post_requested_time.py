# Generated by Django 4.1.5 on 2023-03-07 17:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0059_post_reviewers"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="requested_time",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 7, 17, 45, 54, 448601)
            ),
        ),
    ]
