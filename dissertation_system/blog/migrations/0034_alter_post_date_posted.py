# Generated by Django 4.1.5 on 2023-02-17 12:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0033_remove_tag_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="date_posted",
            field=models.DateTimeField(),
        ),
    ]
