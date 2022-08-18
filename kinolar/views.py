from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView


from .models import Actor, Category, Movie
from .forms import ReviewForm


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

class ActorDetailView(DetailView):
    """Bitta Aktyor uchun""" 
    model = Actor
    slug_field: str = "name"
    template_name: str = "movies/actor.html"  
