"""Forms for adding and editing albums."""

from django import forms

from .models import Album


class AlbumForm(forms.ModelForm):
    """ModelForm covering every user-editable field on an Album."""

    class Meta:
        model = Album
        fields = [
            "title",
            "artist",
            "release_year",
            "genre",
            "format",
            "rating",
            "is_favourite",
            "cover_image_url",
            "notes",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Rumours"}),
            "artist": forms.TextInput(attrs={"placeholder": "e.g. Fleetwood Mac"}),
            "release_year": forms.NumberInput(attrs={"placeholder": "1977", "min": 1900, "max": 2100}),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "cover_image_url": forms.URLInput(attrs={"placeholder": "https://\u2026"}),
            "notes": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "What do you love about this album? When does it hit best?",
                }
            ),
        }
