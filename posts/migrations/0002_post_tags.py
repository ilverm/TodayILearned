# Generated by Django 4.1.11 on 2023-11-16 19:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tags", "0001_initial"),
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(to="tags.tag"),
        ),
    ]