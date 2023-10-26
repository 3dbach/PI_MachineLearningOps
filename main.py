from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡API de la empresa!"}
# Suponemos que ya has cargado tu DataFrame en una variable 'df'

@app.get("/developer/{desarrollador}")
def developer(desarrollador: str):
    # Aquí iría el código para procesar y devolver los datos según el desarrollador.
    def developer(desarrollador: str) -> pd.DataFrame:
    # Filtrar el DataFrame para el desarrollador especificado
    developer_df = steam_games[steam_games['developer'] == desarrollador]
    
    # Agrupar por año
    grouped = developer_df.groupby('year')
    
    # Contar la cantidad total de juegos por año
    total_games = grouped.size()
    
    # Contar la cantidad de juegos que son "Free to Play" o "Free To Play" por año
    free_games = developer_df[developer_df['price'].isin(['Free to Play', 'Free To Play'])].groupby('year').size()
    
    # Crear un DataFrame con los resultados
    result = pd.DataFrame({
        'Año': total_games.index,
        'Cantidad de Items': total_games.values,
        'Contenido Free': (free_games / total_games * 100).fillna(0).round(2)
    }).reset_index(drop=True)
    
    return result

# Test de la función con un ejemplo
developer("Kotoshiro")


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
