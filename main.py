from fastapi import FastAPI
import pandas as pd


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "¡API de Omar Bach!"}

# carga de dataset1 para la funcion 1
steam_games_df1 = pd.read_csv("./data/dataset_uno.csv", encoding="utf-8")

# Cargar el dataframe dos
final_df = pd.read_csv('./data/dataset_dos_limpio.csv', encoding="utf-8")

#carga de los dataframes para el endpoint tres

# Cargar el archivo steam_games
steam_games_cleaned= pd.read_csv("./data/dataset_tres_games.csv", encoding="utf-8")

# Cargar el archivo items
items_cleaned= pd.read_csv("./data/dataset_tres_items_reducido.csv", encoding="utf-8")


# Cargar el archivo user_reviews.csv y mostrar las primeras filas
user_reviews_df = pd.read_csv("./data/user_reviews.csv", encoding="utf-8")
user_reviews_df.head()

# Cargar el archivo steam_games.csv y mostrar las primeras filas
steam_games_df = pd.read_csv("./data/steam_games.csv", encoding="utf-8")
steam_games_df.head()

# Cargar el archivo items_muestramitad.csv y mostrar las primeras filas
items_muestramitad_df = pd.read_csv("./data/items_muestramitad.csv", encoding="utf-8")
items_muestramitad_df.head()

steam_games_df1['release_date'] = pd.to_datetime(steam_games_df1['release_date'], errors='coerce', infer_datetime_format=True)
steam_games_df1['year'] = steam_games_df1['release_date'].dt.year


@app.get("/developer/{desarrollador}")
def developer(desarrollador: str):
    # Convertir el nombre del desarrollador a minúsculas para la comparación
    developer_df = steam_games_df1[steam_games_df1['developer'].str.lower() == desarrollador.lower()]

    # Verificar si encontramos registros para el desarrollador
    if developer_df.empty:
        return {"error": "Desarrollador no encontrado"}

    # Agrupar por año
    grouped = developer_df.groupby('year')
        
    # Contar la cantidad total de juegos por año
    total_games_values = grouped.size().astype(int).tolist()  # Convert to Python int
    total_games_index = [int(year) for year in grouped.size().index]  # Convert index to Python int list
        
    # Contar la cantidad de juegos que son "Free to Play" o "Free To Play" por año
    #free_games = developer_df[developer_df['price'].isin(['Free to Play', 'Free To Play'])].groupby('year').size().astype(int).tolist()  # Convert to Python int
        
    # Diccionario con los resultados
   # result = {
    #    'Año': total_games_index,
    #    'Cantidad de Items': total_games_values,
    #    'Contenido Free': [(free / total * 100).round(2) for free, total in zip(free_games, total_games_values)]
    #    }
    #return result

    # Contar la cantidad de juegos que son "Free to Play" (codificados como 0) por año
    free_games = developer_df[developer_df['price'] == 0].groupby('year').size().astype(int).tolist()  # Convert to Python int

    # Diccionario con los resultados
    result = {
        'Año': total_games_index,
        'Cantidad de Items': total_games_values,
        'Contenido Free': [round(free / total * 100, 2) if total else 0 for free, total in zip(free_games, total_games_values)]
    }
    return result



@app.get("/userdata/{User_id}")
def userdata(User_id: str):
    # Filtrar las revisiones del usuario
    user_reviews = final_df[final_df['user_id'] == User_id].copy()  # Usar .copy() para evitar la advertencia

    # Calcular el dinero gastado por el usuario
    # Convertir la columna de precio a float y manejar casos donde el precio es NaN o 'Free To Play'
    user_reviews.loc[:, 'price'] = user_reviews['price'].replace(['Free To Play', 'Free to Play'], 0)
    user_reviews.loc[:, 'price'] = pd.to_numeric(user_reviews['price'], errors='coerce').fillna(0)
    total_spent = user_reviews['price'].sum()

    # Calcular el porcentaje de recomendación
    total_reviews = len(user_reviews)
    recommended_reviews = user_reviews['recommend'].sum()
    recommendation_percentage = (recommended_reviews / total_reviews) * 100 if total_reviews else 0

    # Calcular la cantidad de items del usuario
    total_items = user_reviews['items_count'].iloc[0] if not user_reviews.empty else 0

    return {
        "Usuario": User_id,
        "Dinero gastado": f"{float(total_spent)} USD",   # Convertir explícitamente a float
        "% de recomendación": f"{float(recommendation_percentage):.2f}%",  # Convertir explícitamente a float
        "cantidad de items": int(total_items)  # Convertir explícitamente a int
    }




@app.get("/UserForGenre/{genero}")

def UserForGenre_test(genero: str):
    # Filtrar los juegos que pertenecen al género especificado
    games_in_genre = steam_games_cleaned[steam_games_cleaned['genres'].str.contains(genero, na=False, case=False)]
    
    # Vincular los juegos filtrados con reduced_items_cleaned para obtener las horas jugadas de cada juego por cada usuario
    user_playtime = games_in_genre.merge(items_cleaned, left_on='id', right_on='item_id', how='inner')
    
    # Agrupar por user_id y sumar las horas jugadas para encontrar el usuario con más horas jugadas
    user_total_playtime = user_playtime.groupby('user_id')['playtime_forever'].sum().reset_index()
    top_user = user_total_playtime.sort_values(by='playtime_forever', ascending=False).iloc[0]['user_id']
    
    # Agrupar por release_date y sumar las horas jugadas para cada año
    hours_by_year = user_playtime.groupby(user_playtime['release_date'].dt.year)['playtime_forever'].sum().reset_index()
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