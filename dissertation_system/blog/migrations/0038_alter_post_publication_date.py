# Generated by Django 4.1.5 on 2023-02-17 12:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0037_alter_post_publication_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="publication_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 2, 17, 12, 41, 38, 24859)
            ),
        ),
    ]
