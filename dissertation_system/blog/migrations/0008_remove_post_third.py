# Generated by Django 4.1.5 on 2023-01-17 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_third'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='third',
        ),
    ]