# Generated by Django 4.1.5 on 2023-02-14 18:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0031_remove_thread_primary_tag_messagemodel_primary_tag"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="messagemodel",
            name="primary_tag",
        ),
    ]