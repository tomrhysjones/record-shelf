"""Initial migration for Record Shelf main_app."""

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=60, unique=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Album",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150)),
                ("artist", models.CharField(max_length=150)),
                (
                    "release_year",
                    models.PositiveIntegerField(
                        help_text="Year the album was originally released.",
                        validators=[
                            django.core.validators.MinValueValidator(1900),
                            django.core.validators.MaxValueValidator(2100),
                        ],
                    ),
                ),
                (
                    "format",
                    models.CharField(
                        choices=[
                            ("vinyl", "Vinyl"),
                            ("cd", "CD"),
                            ("cassette", "Cassette"),
                            ("digital", "Digital"),
                        ],
                        default="vinyl",
                        max_length=10,
                    ),
                ),
                (
                    "rating",
                    models.PositiveIntegerField(
                        default=3,
                        help_text="Your rating from 1 to 5 stars.",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                    ),
                ),
                ("notes", models.TextField(blank=True, help_text="Optional review or notes about the album.")),
                ("cover_image_url", models.URLField(blank=True, help_text="Optional. Link to the album's cover art.")),
                ("is_favourite", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="albums",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "genre",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="albums",
                        to="main_app.genre",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
