# Generated by Django 4.1.5 on 2023-02-19 11:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0047_post_publisher"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="version",
        ),
    ]