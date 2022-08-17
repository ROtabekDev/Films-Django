from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Tavsifi", widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Kategoriyalar"""
    list_display = ("id", "name", "url")
    list_display_links = ("name", )

class ReviewInline(admin.TabularInline):
    """Filmdagi kommentlar"""
    model = Reviews
    extra: int=1
    readonly_fields = ("name", "email")

class MovieShotsInline(admin.TabularInline):
    """Filmdagi kadrlar"""
    model = MovieShots
    extra: int=1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"') 

    get_image.short_description = "Rasmi"



@admin.register(Movie)
class MovieaAdmin(admin.ModelAdmin):
    """Kinolar"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewInline] 
    list_editable = ("draft",) 
    readonly_fields = ("get_image",)
    form = MovieAdminForm
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }), 
        (None, {
            "fields": (("year", "premiere", "country"),)
        }), 
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }), 
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }), 
        ("Options", {
            "fields": (("url", "draft"),)
        }), 
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"') 

    get_image.short_description = "Posteri"

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Kommentlar"""
    list_display = ("name", "email", "parent", "movie", "id") 
    readonly_fields = ("name", "email")
   
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Jnarlar"""
    list_display = ("name", "url")

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Jnarlar"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"') 

    get_image.short_description = "Rasmi"

@admin.register(Rating)
class MovieShotsAdmin(admin.ModelAdmin):
    """Jnarlar"""
    list_display = ("star", "ip") 

@admin.register(MovieShots)
class RatingAdmin(admin.ModelAdmin):
    """Jnarlar"""
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"') 

    get_image.short_description = "Rasmi"   
     
admin.site.register(RatingStar)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
