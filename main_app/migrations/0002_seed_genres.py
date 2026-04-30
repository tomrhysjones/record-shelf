"""Seed Record Shelf with a starter set of music genres."""

from django.db import migrations
from django.utils.text import slugify


SEED_GENRES = [
    "Rock",
    "Jazz",
    "Soul",
    "Funk",
    "Folk",
    "Pop",
    "Hip-Hop",
    "R&B",
    "Electronic",
    "Classical",
    "Reggae",
    "Country",
    "Blues",
    "Metal",
    "Indie",
]


def seed_genres(apps, schema_editor):
    Genre = apps.get_model("main_app", "Genre")
    for name in SEED_GENRES:
        Genre.objects.get_or_create(name=name, defaults={"slug": slugify(name)})


def unseed_genres(apps, schema_editor):
    Genre = apps.get_model("main_app", "Genre")
    Genre.objects.filter(name__in=SEED_GENRES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_genres, reverse_code=unseed_genres),
    ]
