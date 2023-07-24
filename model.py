# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 03:03:39 2023

@author: rodrigo
"""

### IMPORTAMOS LIBRERIAS

import pandas as pd
import numpy  as np

from fastapi import FastAPI

import uvicorn

from sklearn.metrics.pairwise        import cosine_similarity
from sklearn.utils.extmath           import randomized_svd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise        import linear_kernel

# Ingestamos el dataframe de tres variables
data = pd.read_csv("data/ds_model.csv")

# Se crea el modelo de Similitud del coseno para un Sistema de recomendación de películas
# Utilizamos solo 5 primeras apariciones
muestra_aleatoria = data.head(5000) 

# Se vectoriza y se crean arrays o matrices que guardan las características de los registros
tfidf = TfidfVectorizer(stop_words='english') 

# Analizamos y extraemos las palabras mas importantes con TF-IDF Y creamos una matriz que representa la
tdfid_matrix = tfidf.fit_transform(muestra_aleatoria['overview']) 

# Se entrena el modelo
# Calculamos la similitud coseno entre todas las descripciones la similitud coseno 
# # es una medida que nos indica cuanto se parecen dos vectores
cosine_similarity = linear_kernel( tdfid_matrix, tdfid_matrix) 

def recomendacion(titulo: str):
    # Buscamos el indice titulo en nuestro datasets
    idx = muestra_aleatoria[muestra_aleatoria['title'] == titulo].index[0] 

    # Accedemos a la fila 'idx' de la matriz 'simitulud coseno' enumeramos filas, creamos lista de 
    # tuplas, donde cada tupla contiene el indice y similitud coseno de la pelicula
    sim_cosine = list(enumerate(cosine_similarity[idx])) 
    
    # Ordenamos la lista de tuplas en funcion de la similitud coseno de manera descendente,
    # guardamos resultados en variable sim_scores                                                             
    sim_scores = sorted(sim_cosine, key=lambda x: x[1], reverse=True) 
    
    # Creamos lista de las 5 mejores primeras peliculas
    similar_indices = [i for i, _ in sim_scores[1:6]] 
    
    # Seleccionamos los titulos segun los indices y los pasamos a una lista
    similar_movies = muestra_aleatoria['title'].iloc[similar_indices].values.tolist() 
    
    # Retornamos la lista
    return similar_movies 