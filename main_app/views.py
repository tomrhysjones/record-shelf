from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AlbumForm
from .models import Album, Genre


def home(request):
    return render(request, 'home.html')


def album_list(request):
    albums = Album.objects.all()

    selected_genre = request.GET.get('genre', '')
    if selected_genre:
        albums = albums.filter(genre__slug=selected_genre)

    query = request.GET.get('q', '')
    if query:
        albums = albums.filter(title__icontains=query)

    return render(request, 'main_app/album_list.html', {
        'albums': albums,
        'genres': Genre.objects.all(),
        'selected_genre': selected_genre,
        'query': query,
    })


def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    return render(request, 'main_app/album_detail.html', {'album': album})


@login_required
def album_create(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner = request.user
            album.save()
            messages.success(request, f"'{album.title}' was added to your shelf.")
            return redirect('albums:detail', pk=album.pk)
    else:
        form = AlbumForm()

    return render(request, 'main_app/album_form.html', {
        'form': form,
        'form_title': 'Add an album',
        'submit_label': 'Save album',
    })


@login_required
def album_update(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if album.owner != request.user:
        return HttpResponseForbidden('You can only edit your own albums.')

    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{album.title}' was updated.")
            return redirect('albums:detail', pk=album.pk)
    else:
        form = AlbumForm(instance=album)

    return render(request, 'main_app/album_form.html', {
        'form': form,
        'form_title': f'Edit: {album.title}',
        'submit_label': 'Save changes',
        'album': album,
    })


@login_required
def album_delete(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if album.owner != request.user:
        return HttpResponseForbidden('You can only delete your own albums.')

    if request.method == 'POST':
        title = album.title
        album.delete()
        messages.success(request, f"'{title}' was removed from your shelf.")
        return redirect('albums:my_shelf')

    return render(request, 'main_app/album_confirm_delete.html', {'album': album})


@login_required
def my_shelf(request):
    albums = Album.objects.filter(owner=request.user)
    return render(request, 'main_app/my_shelf.html', {'albums': albums})
