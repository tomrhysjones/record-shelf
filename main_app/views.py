"""Views for Record Shelf.

The album list and album detail pages are public — guests can browse them.
Adding, updating and deleting albums all require login, and update/delete
additionally require that the logged-in user owns the album.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AlbumForm
from .models import Album, Genre


# ---------------------------------------------------------------------------
# Public landing page
# ---------------------------------------------------------------------------

def home(request):
    """Static welcome page with calls-to-action."""
    return render(request, "home.html")


# ---------------------------------------------------------------------------
# Album list / detail (public)
# ---------------------------------------------------------------------------

def album_list(request):
    """Browse every album on the shelf, with optional genre filter and search."""
    albums = Album.objects.select_related("owner", "genre").all()

    selected_slug = request.GET.get("genre", "").strip()
    if selected_slug:
        albums = albums.filter(genre__slug=selected_slug)

    query = request.GET.get("q", "").strip()
    if query:
        albums = albums.filter(Q(title__icontains=query) | Q(artist__icontains=query))

    context = {
        "albums": albums,
        "genres": Genre.objects.all(),
        "selected_genre": selected_slug,
        "query": query,
    }
    return render(request, "main_app/album_list.html", context)


def album_detail(request, pk):
    """Show a single album."""
    album = get_object_or_404(
        Album.objects.select_related("owner", "genre"),
        pk=pk,
    )
    return render(request, "main_app/album_detail.html", {"album": album})


# ---------------------------------------------------------------------------
# Album CRUD — login required, ownership enforced for edit/delete
# ---------------------------------------------------------------------------

@login_required
def album_create(request):
    if request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner = request.user
            album.save()
            messages.success(request, f"'{album.title}' was added to your shelf.")
            return redirect(album.get_absolute_url())
    else:
        form = AlbumForm()

    return render(
        request,
        "main_app/album_form.html",
        {"form": form, "form_title": "Add an album", "submit_label": "Save album"},
    )


@login_required
def album_update(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if album.owner != request.user:
        return HttpResponseForbidden("You can only edit your own albums.")

    if request.method == "POST":
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{album.title}' was updated.")
            return redirect(album.get_absolute_url())
    else:
        form = AlbumForm(instance=album)

    return render(
        request,
        "main_app/album_form.html",
        {
            "form": form,
            "form_title": f"Edit: {album.title}",
            "submit_label": "Save changes",
            "album": album,
        },
    )


@login_required
def album_delete(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if album.owner != request.user:
        return HttpResponseForbidden("You can only delete your own albums.")

    if request.method == "POST":
        title = album.title
        album.delete()
        messages.success(request, f"'{title}' was removed from your shelf.")
        return redirect("albums:my_shelf")

    return render(
        request,
        "main_app/album_confirm_delete.html",
        {"album": album},
    )


@login_required
def my_shelf(request):
    """Dashboard showing only the current user's albums."""
    albums = (
        Album.objects
        .select_related("genre")
        .filter(owner=request.user)
    )
    return render(request, "main_app/my_shelf.html", {"albums": albums})
