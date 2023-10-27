from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡API de la empresa Omar!"}

# Cargar los datos y preparar el DataFrame
#steam_games = pd.read_csv('steam_games.csv')
#steam_games['release_date'] = pd.to_datetime(steam_games['release_date'], errors='coerce')
#steam_games['year'] = steam_games['release_date'].dt.year

import pandas as pd

# Cargar el archivo user_reviews.csv y mostrar las primeras filas
user_reviews_df = pd.read_csv("user_reviews.csv")
user_reviews_df.head()

# Cargar el archivo steam_games.csv y mostrar las primeras filas
steam_games_df = pd.read_csv("steam_games.csv")
steam_games_df.head()pip 

# Cargar el archivo items_muestramitad.csv y mostrar las primeras filas
items_muestramitad_df = pd.read_csv("items_muestramitad.csv")
items_muestramitad_df.head()

@app.get("/developer/{desarrollador}")
def developer(desarrollador: str):
    try:  
        # Cargar los datos y preparar el DataFrame
        steam_games = pd.read_csv('steam_games.csv')
        steam_games['release_date'] = pd.to_datetime(steam_games['release_date'], errors='coerce')
        steam_games['year'] = steam_games['release_date'].dt.year  
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
#def userdata(User_id: str):
    # Aquí iría el código para procesar y devolver los datos del usuario.
    #pass
def userdata(User_id: str):
    # Filtrar las revisiones del usuario en user_reviews.csv
    user_reviews = user_reviews_df[user_reviews_df['user_id'] == User_id]

    # Vincular las revisiones del usuario con steam_games.csv para obtener el precio de cada juego
    user_games = user_reviews.merge(steam_games_df, left_on='item_id', right_on='id', how='left')

    # Calcular el dinero gastado por el usuario
    # Convertir la columna de precio a float y manejar casos donde el precio es 'Free To Play' o NaN
    user_games['price'] = user_games['price'].replace(['Free To Play', 'Free to Play'], 0)
    user_games['price'] = pd.to_numeric(user_games['price'], errors='coerce').fillna(0)
    total_spent = user_games['price'].sum()

    # Calcular el porcentaje de recomendación
    total_reviews = len(user_reviews)
    recommended_reviews = user_reviews['recommend'].sum()
    recommendation_percentage = (recommended_reviews / total_reviews) * 100 if total_reviews else 0

    # Calcular la cantidad de items del usuario en items_muestramitad.csv
    user_items = items_muestramitad_df[items_muestramitad_df['user_id'] == User_id]
    total_items = user_items['items_count'].iloc[0] if not user_items.empty else 0

    return {
        "Usuario": User_id,
        "Dinero gastado": f"{total_spent} USD",
        "% de recomendación": f"{recommendation_percentage:.2f}%",
        "cantidad de items": total_items
    }




@app.get("/UserForGenre/{genero}")

def UserForGenre(genero: str):
    # Filtrar los juegos que pertenecen al género especificado en steam_games.csv
    games_in_genre = steam_games_df[steam_games_df['genres'].str.contains(genero, na=False, case=False)]
    
    # Vincular los juegos filtrados con items_muestramitad.csv para obtener las horas jugadas de cada juego por cada usuario
    user_playtime = games_in_genre.merge(items_muestramitad_df, left_on='id', right_on='item_id', how='inner')
    
    # Agrupar por user_id y sumar las horas jugadas para encontrar el usuario con más horas jugadas
    user_total_playtime = user_playtime.groupby('user_id')['playtime_forever'].sum().reset_index()
    top_user = user_total_playtime.sort_values(by='playtime_forever', ascending=False).iloc[0]['user_id']
    
    # Agrupar por release_date y sumar las horas jugadas para cada año
    hours_by_year = user_playtime.groupby(user_playtime['release_date'].str[:4])['playtime_forever'].sum().reset_index()
    hours_by_year = hours_by_year.rename(columns={"release_date": "Año", "playtime_forever": "Horas"})
    
    # Convertir el DataFrame a una lista de diccionarios
    hours_list = hours_by_year.to_dict('records')
    
    return {
        "Usuario con más horas jugadas para Género {}".format(genero): top_user,
        "Horas jugadas": hours_list
    }




@app.get("/best_developer_year/{año}")

def best_developer_year(año: int):
    # Filtrar los juegos que fueron lanzados en el año especificado
    games_of_year = steam_games_df[steam_games_df['release_date'].str.startswith(str(año), na=False)]
    
    # Vincular los juegos filtrados con user_reviews.csv para obtener las revisiones
    recommended_reviews = games_of_year.merge(user_reviews_df, left_on='id', right_on='item_id', how='inner')
    
    # Filtrar las revisiones que tienen recommend como True
    recommended_reviews = recommended_reviews[recommended_reviews['recommend'] == True]
    
    # Agrupar por developer y contar las recomendaciones
    developer_counts = recommended_reviews.groupby('developer').size().reset_index(name='recommendations')
    top_developers = developer_counts.sort_values(by='recommendations', ascending=False).head(3)
    
    # Preparar la lista de resultados
    results = [{"Puesto {}".format(i+1): dev} for i, dev in enumerate(top_developers['developer'])]
    
    return results




@app.get("/developer_reviews_analysis/{desarrolladora}")

def developer_reviews_analysis(desarrolladora: str):
    # Filtrar los juegos que fueron desarrollados por la desarrolladora especificada
    developer_games = steam_games_df[steam_games_df['developer'] == desarrolladora]
    
    # Vincular los juegos filtrados con user_reviews.csv para obtener las reseñas
    developer_reviews = developer_games.merge(user_reviews_df, left_on='id', right_on='item_id', how='inner')
    
    # Clasificar las reseñas en "Positive" y "Negative" basado en la columna recommend
    developer_reviews['sentiment'] = developer_reviews['recommend'].apply(lambda x: 'Positive' if x else 'Negative')
    
    # Contar la cantidad de reseñas "Positive" y "Negative"
    sentiment_counts = developer_reviews['sentiment'].value_counts().to_dict()
    
    return {desarrolladora: sentiment_counts}