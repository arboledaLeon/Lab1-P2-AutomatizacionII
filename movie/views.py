from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie 

import matplotlib.pyplot as plt 
import matplotlib 
import io 
import urllib, base64 

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'León ArboledaG'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains = searchTerm)
    else:
        movies = Movie.objects.all()
    return render (request, 'home.html', {'searchTerm': searchTerm, 'movies': movies, 'name':'León Arboleda G'})


#def about(request):
    #return HttpResponse("This is the About Page")
def about(request):
    return HttpResponse('<h1>Welcome to About Page </h1>')

def signup(request):
    email = request.GET.get('email', '')
    return render(request, 'signup.html', {'email': email}) 

def statistics_view(request):
    matplotlib.use('Agg')
    
    # ===== GRÁFICA POR AÑO =====
    all_movies = Movie.objects.all()
    movie_counts_by_year = {}
    
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    # ===== GRÁFICA POR GÉNERO =====
    movie_counts_by_genre = {}
    
    for movie in all_movies:
        # Tomar solo el primer género (si los géneros están separados por comas)
        if movie.genre:
            # Dividir por comas y tomar el primer género
            genres = movie.genre.split(',')
            first_genre = genres[0].strip() if genres else "No genre"
        else:
            first_genre = "No genre"
            
        if first_genre in movie_counts_by_genre:
            movie_counts_by_genre[first_genre] += 1
        else:
            movie_counts_by_genre[first_genre] = 1

    # Crear figura con dos subgráficas
    plt.figure(figsize=(15, 6))
    
    # PRIMERA GRÁFICA - Por año
    plt.subplot(1, 2, 1)  # 1 fila, 2 columnas, primer gráfico
    bar_positions_year = range(len(movie_counts_by_year))
    plt.bar(bar_positions_year, movie_counts_by_year.values(), width=0.5, align='center', color='skyblue')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions_year, movie_counts_by_year.keys(), rotation=90)
    
    # SEGUNDA GRÁFICA - Por género
    plt.subplot(1, 2, 2)  # 1 fila, 2 columnas, segundo gráfico
    bar_positions_genre = range(len(movie_counts_by_genre))
    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=0.5, align='center', color='lightcoral')
    plt.title('Movies per Genre (First Genre Only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=45)
    
    # Ajustar el layout para que no se superpongan
    plt.tight_layout()
    
    # Guardar la gráfica
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    # Convertir a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    return render(request, 'statistics.html', {'graphic': graphic})





