from django.urls import path

from . import views 

urlpatterns = [
    path('', views.MoviesView.as_view(), name='movies-list'),
    path("filter/", views.FilterMoviesView.as_view(), name="filter"),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add-review'),
    path('actor/<str:slug>/', views.ActorDetailView.as_view(), name='actor-detail'),
]