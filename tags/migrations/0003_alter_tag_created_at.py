# Generated by Django 4.1.11 on 2024-02-06 14:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tags", "0002_tag_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="created_at",
            field=models.DateField(auto_now_add=True),
        ),
    ]
