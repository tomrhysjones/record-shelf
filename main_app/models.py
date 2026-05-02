from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Album(models.Model):
    FORMAT_CHOICES = [
        ('vinyl', 'Vinyl'),
        ('cd', 'CD'),
        ('cassette', 'Cassette'),
        ('digital', 'Digital'),
    ]

    title = models.CharField(max_length=150)
    artist = models.CharField(max_length=150)
    release_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='vinyl')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3
    )
    notes = models.TextField(blank=True)
    cover_image_url = models.URLField(blank=True)
    is_favourite = models.BooleanField(default=False)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='albums')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.artist}'

    def get_absolute_url(self):
        return reverse('albums:detail', kwargs={'pk': self.pk})

    def stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)