# Generated by Django 4.1.5 on 2023-03-05 10:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0056_remove_post_htmlfile_alter_post_primary_tag_and_more"),
        ("users", "0015_remove_profile_f_name_remove_profile_l_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="to_review",
            field=models.ManyToManyField(
                blank=True, related_name="to_review", to="blog.tag"
            ),
        ),
    ]
