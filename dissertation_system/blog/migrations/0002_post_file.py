# Generated by Django 4.1.5 on 2023-01-17 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file',
            field=models.FileField(default='default.jpg', upload_to='documents/'),
        ),
    ]
