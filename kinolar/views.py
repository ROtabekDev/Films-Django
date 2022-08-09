from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView


from .models import Movie


# class MoviesView(View):
#     """Barcha filmlar ro`yhati"""
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, "movies/movies.html", {"movie_list": movies})

class MoviesView(ListView):
    """Barcha filmlar ro`yhati"""
    model = Movie
    movies = Movie.objects.filter(draft=False)
    template_name: str="movies/movies.html" 

# class MovieDetailView(View):
#     """Bitta film uchun"""
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, "movies/movie_detail.html", {"movie": movie})

class MovieDetailView(DetailView):
    """Bitta film uchun""" 
    model = Movie
    slug_field: str = "url"
    template_name: str = "movies/movie_detail.html" 

