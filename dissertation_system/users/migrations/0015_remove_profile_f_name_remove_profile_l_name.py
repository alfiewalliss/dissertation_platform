# Generated by Django 4.1.5 on 2023-02-17 12:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0014_profile_f_name_profile_l_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="f_name",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="l_name",
        ),
    ]