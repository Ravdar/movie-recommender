# Generated by Django 4.2.9 on 2024-01-28 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0005_recommendation"),
    ]

    operations = [
        migrations.RemoveField(model_name="recommendation", name="if_random",),
        migrations.AddField(
            model_name="recommendation",
            name="datetime_of_prompt",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
