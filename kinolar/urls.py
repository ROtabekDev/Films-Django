from django.urls import path

from . import views 

urlpatterns = [
    path('', views.MoviesView.as_view(), name='movies-list'),
    path('<slug:slug>', views.MovieDetailView.as_view(), name='movie-detail'),
]