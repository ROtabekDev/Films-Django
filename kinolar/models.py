from django.db import models
from datetime import date
from django.urls import reverse
class Category(models.Model):
    """Kategoriya"""
    name = models.CharField('Nomi', max_length=150)
    description = models.TextField("Tevsifi")
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta: 
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

class Actor(models.Model):
    """Aktyorlar va rejissorlar"""
    name = models.CharField("Ismi", max_length=100)
    age = models.PositiveSmallIntegerField("Yoshi", default=0)
    description = models.TextField("Tavsifi")
    image = models.ImageField("Rasmi", upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta: 
        verbose_name = 'Aktyorlar va rejissorlar'
        verbose_name_plural = 'Aktyorlar va rejissorlar'

class Genre(models.Model):
    """Janrlar"""
    name = models.CharField('Nomi', max_length=100)
    description = models.TextField("Tevsifi")
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta: 
        verbose_name = 'Janr'
        verbose_name_plural = 'Janrlar'

class Movie(models.Model):
    """Kino"""
    title = models.CharField("Nomi", max_length=100)
    tagline = models.CharField("Qisqacha tavsif", max_length=100, default="")
    description = models.TextField('Tavsifi')
    poster = models.ImageField('Poster', upload_to="movies/")
    year = models.PositiveSmallIntegerField("Chiqarilgan yili", default=2019)
    country = models.CharField('Mamlakati', max_length=50)
    directors = models.ManyToManyField(Actor, verbose_name='rejissorlar', related_name='kino_direktor')
    actors = models.ManyToManyField(Actor, verbose_name='aktyorlar', related_name='kino_aktyor')
    genres = models.ManyToManyField(Genre, verbose_name='janrlar')
    premiere = models.DateField("Primyerasi", default=date.today)
    budget = models.PositiveIntegerField("Sarflangan pul", default=0, help_text="Summani dollarda ko`rsating")
    fees_in_usa = models.PositiveIntegerField(
        "AQSh uchun to`lov", default=0, help_text="Summani dollarda ko`rsating"
        )
    fees_in_world = models.PositiveIntegerField(
        "Dunyo uchun to`lov", default=0, help_text="Summani dollarda ko`rsating"
        )
    category = models.ForeignKey(
        Category, verbose_name='Kategoriya', on_delete=models.SET_NULL, null=True, blank=True
    )
    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField('Qoralama', default=False)

    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse('movie-detail', kwargs={'slug': self.url})

    def get_reviews(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta: 
        verbose_name = 'Kino'
        verbose_name_plural = 'Kinolar'

class MovieShots(models.Model):
    """Kinodan kadrlar"""
    title = models.CharField("Nomi", max_length=100)
    description = models.TextField('Tavsifi')
    image = models.ImageField('Poster', upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name='Kino', on_delete=models.CASCADE)
 

    def __str__(self):
        return self.title

    class Meta: 
        verbose_name = 'Filmdan kadr'
        verbose_name_plural = 'Filmdan kadrlar'

class RatingStar(models.Model):
    """Reyting yulduzi"""
    value = models.SmallIntegerField("Qiymati", default=0) 
 

    def __str__(self):
        return self.value

    class Meta: 
        verbose_name = 'Reyting yulduz'
        verbose_name_plural = 'Reyting yulduzlar'

class Rating(models.Model):
    """Reyting"""
    ip = models.CharField("IP addresi", max_length=30) 
    star = models.ForeignKey(RatingStar, verbose_name='Yulduzi', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name='Kino', on_delete=models.CASCADE)
 

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta: 
        verbose_name = 'Reyting'
        verbose_name_plural = 'Reytinglar'

class Reviews(models.Model):
    """Kommentlar"""
    email = models.EmailField()
    name = models.CharField("Ismi", max_length=100)
    text = models.TextField("Xabar", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='OtaKlass', on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(Movie, verbose_name='Kino', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta: 
        verbose_name = 'Komment'
        verbose_name_plural = 'Kommentlar'




