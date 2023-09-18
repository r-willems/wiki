from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.view_entry, name="entry"),
    path("search/", views.search, name="search"),
    path("editor/", views.editor, name="editor"),
    path("random/", views.random_page, name="random"),
    path("submit/", views.submit, name="submit")
]
