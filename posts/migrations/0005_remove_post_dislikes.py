# Generated by Django 4.1.11 on 2023-12-07 07:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0004_post_dislikes_post_likes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="dislikes",
        ),
    ]
