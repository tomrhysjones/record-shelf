from django import forms
from .models import Album


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = [
            'title',
            'artist',
            'release_year',
            'genre',
            'format',
            'rating',
            'is_favourite',
            'cover_image_url',
            'notes',
        ]