# Generated by Django 4.1.5 on 2023-02-17 14:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0041_remove_post_publication_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="publication_date",
            field=models.DateField(
                default=datetime.datetime(2023, 2, 17, 14, 43, 58, 551905)
            ),
        ),
    ]
