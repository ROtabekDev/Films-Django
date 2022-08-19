from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import HttpResponse

from .models import Actor, Category, Movie, Genre, Rating
from .forms import RatingForm, ReviewForm


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
    paginate_by: int=3

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context 

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
    """Filtr"""
    template_name: str="movies/movies.html"  
    paginate_by: int=2

    def get_queryset(self): 
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre") ) 
            ).distinct()
        return queryset

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context['genre'] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context

class AddStarRating(View):
    """Filmga star qo`yish""" 
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

    
class Search(GenreYear, ListView): 
    """Qidiruv"""
    template_name: str="movies/movies.html"  
    paginate_by: int=3

    def get_queryset(self):  
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))
        
    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context
