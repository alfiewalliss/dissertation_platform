# Generated by Django 4.1.5 on 2023-02-17 14:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0038_alter_post_publication_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="publication_date",
            field=models.DateField(),
        ),
    ]