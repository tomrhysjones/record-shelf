"""Smoke tests for the Record Shelf app.

Covers: model basics, list/detail visibility, login-required CRUD, and
ownership-enforced edit/delete.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Album, Genre


class AlbumFlowTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="abc12345!")
        self.bob = User.objects.create_user(username="bob", password="abc12345!")
        self.rock = Genre.objects.create(name="Rock")
        self.album = Album.objects.create(
            title="Rumours",
            artist="Fleetwood Mac",
            release_year=1977,
            format=Album.FORMAT_VINYL,
            rating=5,
            notes="An all-timer.",
            owner=self.alice,
            genre=self.rock,
        )

    def test_album_str_and_stars(self):
        self.assertEqual(str(self.album), "Rumours \u2014 Fleetwood Mac")
        self.assertEqual(self.album.stars, "\u2605\u2605\u2605\u2605\u2605")

    def test_list_is_public(self):
        response = self.client.get(reverse("albums:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rumours")

    def test_create_requires_login(self):
        response = self.client.get(reverse("albums:create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_only_owner_can_edit(self):
        self.client.login(username="bob", password="abc12345!")
        response = self.client.get(reverse("albums:update", args=[self.album.pk]))
        self.assertEqual(response.status_code, 403)

    def test_only_owner_can_delete(self):
        self.client.login(username="bob", password="abc12345!")
        response = self.client.post(reverse("albums:delete", args=[self.album.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Album.objects.filter(pk=self.album.pk).exists())

    def test_owner_can_delete(self):
        self.client.login(username="alice", password="abc12345!")
        response = self.client.post(reverse("albums:delete", args=[self.album.pk]))
        self.assertRedirects(response, reverse("albums:my_shelf"))
        self.assertFalse(Album.objects.filter(pk=self.album.pk).exists())
