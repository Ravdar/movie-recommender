# Generated by Django 4.2.9 on 2024-02-14 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0007_alter_recommendation_response_time"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("error", "Error/bug"),
                            ("feedback", "Feedback"),
                            ("question", "Question"),
                            ("other", "Other"),
                        ],
                        max_length=40,
                    ),
                ),
                ("mail", models.CharField(max_length=20)),
                ("content", models.TextField()),
            ],
        ),
    ]
