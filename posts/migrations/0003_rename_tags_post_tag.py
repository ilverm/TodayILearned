# Generated by Django 4.1.11 on 2023-11-16 19:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0002_post_tags"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="tags",
            new_name="tag",
        ),
    ]