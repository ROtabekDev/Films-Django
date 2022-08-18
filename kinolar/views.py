from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Actor, Category, Movie, Genre
from .forms import ReviewForm


class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year").order_by("-year")

    
# class MoviesView(View):
#     """Barcha filmlar ro`yhati"""
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, "movies/movies.html", {"movie_list": movies})

class MoviesView(GenreYear, ListView):
    """Barcha filmlar ro`yhati"""
    model = Movie
    movies = Movie.objects.filter(draft=False)
    template_name: str="movies/movies.html"  

# class MovieDetailView(View):
#     """Bitta film uchun"""
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, "movies/movie_detail.html", {"movie": movie})

class MovieDetailView(GenreYear, DetailView):
    """Bitta film uchun""" 
    model = Movie
    slug_field: str = "url"
    template_name: str = "movies/movie_detail.html"  

class AddReview(View):
    """Kommentlar"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save() 
        return redirect(movie.get_absolute_url())

class ActorDetailView(GenreYear, DetailView):
    """Bitta Aktyor uchun""" 
    model = Actor
    slug_field: str = "name"
    template_name: str = "movies/actor.html"  


class FilterMoviesView(GenreYear, ListView): 
    template_name: str="movies/movies.html"  
    """Filtr"""
    def get_queryset(self):
        print("rungoooooooooooooooooooooooooooooooooooo")
        print(self.request.GET.getlist("genre"))
        print(self.request.GET.getlist("year"))
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre") ) 
            )
        print(queryset)
        return queryset
