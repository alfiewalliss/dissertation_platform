# Generated by Django 4.1.5 on 2023-02-08 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='admin',
            field=models.IntegerField(default=0),
        ),
    ]
