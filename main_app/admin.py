"""Register Record Shelf models with the Django admin so we can seed Genres."""

from django.contrib import admin

from .models import Album, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "release_year", "genre", "owner", "rating", "format")
    list_filter = ("genre", "format", "is_favourite")
    search_fields = ("title", "artist")
