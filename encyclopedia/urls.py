from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create/", views.create, name="create"),
    path("wiki/<str:title>/entry", views.edit, name="edit"),
    path("wiki/<str:title>/submit", views.submitEdit, name="submitEdit"),
    path("random/", views.randomPage, name="random"),
    path("search/", views.search, name="search")
]
