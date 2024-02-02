# Generated by Django 4.2.9 on 2024-01-24 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "mainapp",
            "0003_movie_amazon_prime_movie_apple_tv_movie_disney_plus_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="movie", old_name="imdb_link", new_name="tmdb_link",
        ),
        migrations.RemoveField(model_name="movie", name="amazon_prime",),
        migrations.RemoveField(model_name="movie", name="apple_tv",),
        migrations.RemoveField(model_name="movie", name="disney_plus",),
        migrations.RemoveField(model_name="movie", name="hbo_max",),
        migrations.RemoveField(model_name="movie", name="hulu",),
        migrations.RemoveField(model_name="movie", name="netflix",),
        migrations.RemoveField(model_name="movie", name="peacock",),
        migrations.AddField(
            model_name="movie",
            name="description",
            field=models.CharField(default=0, max_length=5000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="movie",
            name="streaming_services",
            field=models.CharField(default=0, max_length=10000),
            preserve_default=False,
        ),
    ]
