"""Views for account creation. Login/logout use Django's built-ins."""

from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import SignUpForm


def signup(request):
    """Create a new user account, log them in, and redirect to the album list."""
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("albums:list")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})
