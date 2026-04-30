"""Database models for the Record Shelf app.

Two models live here besides Django's built-in User:

  * Genre — a simple lookup (Rock, Jazz, Soul, Folk, …) so users can classify
    each album and filter the browse page by genre.
  * Album — the main entity, owned by a single User and belonging to one Genre.
"""

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Genre(models.Model):
    """A high-level grouping used to organise albums."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Album(models.Model):
    """A user-owned album in someone's record shelf."""

    FORMAT_VINYL = "vinyl"
    FORMAT_CD = "cd"
    FORMAT_CASSETTE = "cassette"
    FORMAT_DIGITAL = "digital"
    FORMAT_CHOICES = [
        (FORMAT_VINYL, "Vinyl"),
        (FORMAT_CD, "CD"),
        (FORMAT_CASSETTE, "Cassette"),
        (FORMAT_DIGITAL, "Digital"),
    ]

    title = models.CharField(max_length=150)
    artist = models.CharField(max_length=150)

    release_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        help_text="Year the album was originally released.",
    )

    format = models.CharField(
        max_length=10,
        choices=FORMAT_CHOICES,
        default=FORMAT_VINYL,
    )

    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        help_text="Your rating from 1 to 5 stars.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Optional review or notes about the album.",
    )

    cover_image_url = models.URLField(
        blank=True,
        help_text="Optional. Link to the album's cover art.",
    )

    is_favourite = models.BooleanField(default=False)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="albums",
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        related_name="albums",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} \u2014 {self.artist}"

    def get_absolute_url(self):
        return reverse("albums:detail", kwargs={"pk": self.pk})

    @property
    def stars(self):
        """Return a string of filled and empty stars for templates."""
        filled = "\u2605" * self.rating
        empty = "\u2606" * (5 - self.rating)
        return filled + empty
