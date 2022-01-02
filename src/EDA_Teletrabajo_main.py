import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from EDA_Teletrabajo_functions import *

# ----------------------------------------------------------------------------------------------------------------------
# Cuerpo principal streamlib
st.set_page_config(page_title="El potencial económico del teletrabajo",
                   page_icon=":plug:",
                   layout="centered",
                   initial_sidebar_state="auto")

# Cargamos los datos necesarios para las visualizaciones
dfcomplete = pd.read_csv("data/datos completos.csv", sep = ';',index_col = 0)
dfcomplete.head()

alquiler = pd.read_csv("data/variacion alquiler.csv", sep = ';',index_col = 0)
alquiler = alquiler.T
alquiler.reset_index(inplace = True)
alquiler.rename(columns = {'index' : 'Meses'}, inplace = True)
alquiler.index.provincias = None
alquiler.head()

df = pd.read_csv("data/datos simplificados.csv", sep = ';',index_col = 0)
df['Precio m2 Alquiler'][2] = 7.5
df.rename(columns = {'Salario media': 'S Medio'}, inplace= True)
df.reset_index(inplace = True)
df.head()

comunidades = pd.read_csv("data/comunidades salario, afiliadosSS y coste.csv", sep = ';', index_col = 0)
comunidades = comunidades.T
comunidades.reset_index(inplace = True)
comunidades.rename(columns = {'index': 'provincias' }, inplace = True)
comunidades.head()

plt.figure(figsize=(10,10))
sns.heatmap(df.corr(),vmin=-1, vmax=1, center=0,
            cmap=sns.diverging_palette(220, 20, as_cmap=True),
            square=True, linewidths=.5, annot = True)

# Menu streamlit para moverse por las diferentes partes del EDA
menu = st.sidebar.selectbox("Menu:",('Home', 'Situación mercado laboral', 'Rendimiento salario', 'Donde vivir', 'Calculadora hipoteca', 'Conclusiones'))
if 'check' not in st.session_state:
    st.session_state.check = 0


if menu == 'Home':
    home(df)
    st.session_state.check = 0
elif menu == 'Situación mercado laboral':
    pulso(df, alquiler, comunidades)
    st.session_state.check = 0

elif menu == 'Rendimiento salario':
    rendimiento(df,comunidades)
    st.session_state.check = 0
elif menu == 'Donde vivir':
    vivir(df, alquiler)
    st.session_state.check = 0
elif menu == 'Calculadora hipoteca':
    calculadora_hipoteca()
elif menu == 'Conclusiones':
    conclusiones()
