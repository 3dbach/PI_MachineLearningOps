from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡API de la empresa!"}

# Cargar los datos y preparar el DataFrame
steam_games = pd.read_csv('steam_games.csv')
steam_games['release_date'] = pd.to_datetime(steam_games['release_date'], errors='coerce')
steam_games['year'] = steam_games['release_date'].dt.year

@app.get("/developer/{desarrollador}")
def developer(desarrollador: str):
    try:    
        # Convertir el nombre del desarrollador a minúsculas para la comparación
        developer_df = steam_games[steam_games['developer'].str.lower() == desarrollador.lower()]

        # Verificar si encontramos registros para el desarrollador
        if developer_df.empty:
            return {"error": "Desarrollador no encontrado"}

        # Agrupar por año
        grouped = developer_df.groupby('year')
        
        # Contar la cantidad total de juegos por año
        total_games = grouped.size()
        
        # Contar la cantidad de juegos que son "Free to Play" o "Free To Play" por año
        free_games = developer_df[developer_df['price'].isin(['Free to Play', 'Free To Play'])].groupby('year').size()
        
        # Crear un diccionario con los resultados
        result = {
            'Año': list(total_games.index),
            'Cantidad de Items': list(total_games.values),
            'Contenido Free': list((free_games / total_games * 100).fillna(0).round(2))
        }
        print(steam_games.head())  # Verifica si el DataFrame se cargó correctamente
        print(developer_df)  # Verifica si el filtrado por desarrollador funciona

        return result
    except Exception as e:
        return {"error": str(e)}

"""
# Cargar los datos y preparar el DataFrame (como en el notebook)
steam_games = pd.read_csv('steam_games.csv')
steam_games['release_date'] = pd.to_datetime(steam_games['release_date'], errors='coerce')
steam_games['year'] = steam_games['release_date'].dt.year

@app.get("/developer/{desarrollador}")
def developer(desarrollador: str):
    # Filtrar el DataFrame para el desarrollador especificado
    developer_df = steam_games[steam_games['developer'] == desarrollador]
    
    # Agrupar por año
    grouped = developer_df.groupby('year')
    
    # Contar la cantidad total de juegos por año
    total_games = grouped.size()
    
    # Contar la cantidad de juegos que son "Free to Play" o "Free To Play" por año
    free_games = developer_df[developer_df['price'].isin(['Free to Play', 'Free To Play'])].groupby('year').size()
    
    # Crear un DataFrame con los resultados
    result = {
        'Año': list(total_games.index),
        'Cantidad de Items': list(total_games.values),
        'Contenido Free': list((free_games / total_games * 100).fillna(0).round(2))
    }
    
    return result
"""
@app.get("/userdata/{User_id}")
def userdata(User_id: str):
    # Aquí iría el código para procesar y devolver los datos del usuario.
    pass

@app.get("/UserForGenre/{genero}")
def UserForGenre(genero: str):
    # Aquí iría el código para procesar y devolver los datos del género.
    pass

@app.get("/best_developer_year/{año}")
def best_developer_year(año: int):
    # Aquí iría el código para procesar y devolver el top 3 de desarrolladores para el año dado.
    pass

@app.get("/developer_reviews_analysis/{desarrolladora}")
def developer_reviews_analysis(desarrolladora: str):
    # Aquí iría el código para procesar y devolver el análisis de reseñas para el desarrollador.
    pass
