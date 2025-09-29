
from django.core.management.base import BaseCommand
from movie.models import Movie
import json
import os

class Command(BaseCommand):
    help = 'Load movies from JSON file into database'

    def handle(self, *args, **options):
        # Obtener la ruta del archivo JSON
        json_file = os.path.join(os.path.dirname(__file__), 'movies.json')
        
        try:
            # Abrir y leer el archivo JSON
            with open(json_file, 'r', encoding='utf-8') as file:
                movies_data = json.load(file)
            
            # Procesar las primeras 100 películas
            count = 0
            for movie_data in movies_data[:100]:
                try:
                    # Crear instancia de Movie
                    movie = Movie(
                        title=movie_data.get('title', 'Sin título'),
                        description=movie_data.get('description', 'Sin descripción'),
                        genre=movie_data.get('genre', 'Sin género'),
                        year=movie_data.get('year', 0),
                    )
                    movie.save()
                    count += 1
                    
                    if count % 10 == 0:
                        self.stdout.write(f'Procesadas {count} películas...')
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Error procesando película: {e}')
                    )
                    continue
            
            self.stdout.write(
                self.style.SUCCESS(f'¡Éxito! Se cargaron {count} películas a la base de datos.')
            )
            
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR('Error: No se encontró el archivo movies.json')
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR('Error: El archivo JSON está corrupto')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error inesperado: {e}')
            )