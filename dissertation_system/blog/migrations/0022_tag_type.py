# Generated by Django 4.1.5 on 2023-02-08 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_tag_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='type',
            field=models.CharField(choices=[('User', 'USER'), ('Post', 'POST')], default='Post', max_length=4),
        ),
    ]