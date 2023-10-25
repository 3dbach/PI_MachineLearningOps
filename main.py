from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Suponemos que ya has cargado tu DataFrame en una variable 'df'

@app.get("/developer/{desarrollador}")
def developer(desarrollador: str):
    # Aquí iría el código para procesar y devolver los datos según el desarrollador.
    pass

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
