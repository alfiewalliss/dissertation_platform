# Generated by Django 4.1.5 on 2023-02-14 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0030_thread_primary_tag"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="thread",
            name="primary_tag",
        ),
        migrations.AddField(
            model_name="messagemodel",
            name="primary_tag",
            field=models.ForeignKey(
                default=23, on_delete=django.db.models.deletion.CASCADE, to="blog.tag"
            ),
        ),
    ]
