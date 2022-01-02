import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



# Función para incorporar dentro de las figuras,
# los valores al final de los barplot
# Parametro obligatorio  la figura
# Parametro opcional :H V en funcion de diagrama de barra horizontal o vertical
# Parametro opcional: la separación

def show_values_on_bars(axs, h_v="v", space=0.4):
    def _show_on_single_plot(ax):
        if h_v == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height()
                value = float(p.get_height())
                ax.text(_x, _y, value, ha="center")
        elif h_v == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height()
                value = float(p.get_width())
                ax.text(_x, _y, value, ha="left")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax)
    else:
        _show_on_single_plot(axs)


# Portada con heatmap del streamlit
def home(df):
    st.title("El potencial económico del teletrabajo")
    st.write("Visión general del teletrabajo.")
    st.image("images/teletrabajo.jpeg")

    with st.beta_expander("Idea General"):
        st.write('El teletrabajo antes del covid se situaba en una media europea de casi el 15% en europa, '
                 'con una clara ventaja en los paises nordicos,con una media del 30%, destacando Paises Bajos con el '
                 '45% .')
        st.write('En el caso de España la media precovid se situaba en el 7%, no obstante según el paper del Banco de '
                 'España: '
                 'Artículos analiticos 2/2020 El Teletrabajo en España, '
                 'tenemos un potencial para teletrabajar del 30% del mercado laboral y un 50% en profesiones '
                 'intelectuales')
        st.write('Con un potencial tan alto y una población tan poco adaptada al teletrabajo, además de las ventajas '
                 'como la conciliación etc... '
                 'el planteamiento de este EDA es el siguiente:')
        st.write('Verificar el potencial económico y la posiblidad de elegir tu lugar de residencia en base a '
                 'preferencias personales y no laborales, '
                 'lo que nos va a llevar a analizar los siguientes puntos')
        st.write('-Análisis genérico de la situación  del mercado laboral en función de la tasa de paro y los afiliados '
                 'a la seguridad social')
        st.write('-Rendimiento del salario en las diferences provincias, pudiendo valorar el cambio de poder '
                 'adquisitivo según en que provincia estemos ')
        st.write('-Contrastar los precios del mercado inmobiliario para poder valorar donde residir')

        st.image("images/teletrabajo-españa.jpeg")

# heatmap inicial para hablar de algunas correlaciones
    plt.figure(figsize=(10, 10))
    sns.heatmap(df.corr(), vmin=-1, vmax=1, center=0,
                cmap=sns.diverging_palette(220, 20, as_cmap=True),
                square=True, linewidths=.5, annot=True)
    plt.savefig('images/heat.jpeg', dpi=400)
    st.image('images/heat.jpeg')

    with st.beta_expander("Vistazo genérico a los datos"):
        st.write(df.head())

    with st.beta_expander('Conclusiones iniciales:'):
        st.write('-Correlaciones casi perfectas entre m2 escriturado y precio m2, la razón por la que no es perfecta '
                 'como veremos a continuación,  es la fuente de los datos')
        st.write('-Correlación directa alta entre salario, precio de compra y coste de vida')
        st.write('Una posible falsa correlación entre tasa de paro y los precios en 2016')
        st.write('Sobre todo ello hablaremos en las siguientes pestañas.')

# Pagina donde analizar el paro en relación a la seguridad socia
def pulso(df, alquiler, comunidades):

    # -Devuelve tasaparo,
    # -argumento obligatorio dataframe con los datos generados en exploracion de datos
    # -argumentos opcional, start y stop, para seleccionar un conjunto concreto de provincias. Por defecto todo el conjunto.
    # -argumento opcional, orden, para organizar la salida en funcion de otra columna. Por defecto el propio paro
    def paro(df, start=None, stop=None, orden='Tasa Paro '):
        fysize = 10
        if start != None or stop != None:
            fysize = 5
        fig = plt.figure(figsize=(10, fysize), dpi=100)
        ax = fig.gca()
        tasaparo = sns.barplot(x='Tasa Paro ',
                               y='provincias',
                               ax=ax,
                               palette='cool',
                               data=df[:].sort_values(by=orden, ascending=False)[start:stop],
                               ci=None)
        ax.set_ylabel("Provincia")
        ax.set_xlabel("Tasa de paro")
        ax.set_title("Tasa de paro por provincias")
        show_values_on_bars(tasaparo, "h", 0.3)
        return tasaparo

    st.subheader('Situación mercado laboral')
    st.write('Demos un vistazo a la tasa de paro por provincias:')

    # Llamamos a la función, pero dado el funcionamiento de streamlit con seaborn, sería ams viable tener la imagen
    # generada a parte y cargarla.
    paro(df)
    plt.tight_layout()
    plt.savefig('images/tasaparo.jpeg', dpi=500)
    st.image('images/tasaparo.jpeg')

    with st.beta_expander('Pulse si quiere mas parámetros'):
        checkmas = st.checkbox('Ver provincias con mas paro')
        checkmenos = st.checkbox('Ver provincias con menos paro')
        if checkmas:
            paro(df, 0, 20)
            plt.tight_layout()
            plt.savefig('images/tasaparomas.jpeg', dpi=500)
            st.image('images/tasaparomas.jpeg')
        if checkmenos:
            paro(df, 20)
            plt.tight_layout()
            plt.savefig('images/tasaparomenos.jpeg', dpi=500)
            st.image('images/tasaparomenos.jpeg')


    # Devuelve afiliados a la seguridad social
    def afiliados_SS(df, start=None, stop=None, orden='Afiliados SS'):
        fysize = 6
        if start != None or stop != None:
            fysize = 3
        fig = plt.figure(figsize=(14, fysize), dpi=100)
        ax = fig.gca()
        afiliados = sns.barplot(x='Afiliados SS',
                                y='provincias',
                                ax=ax,
                                palette='cool',
                                data=df[:].sort_values(by=orden, ascending=False)[start:stop],
                                ci=None)
        ax.set_ylabel("comunidades")
        ax.set_xlabel("Afiliados")
        ax.set_title("Afiliados SS por comunidad")
        show_values_on_bars(afiliados, "h", 0.3)
        return afiliados

    st.write('Veamos los afiliados a la seguridad social por comunidades')
    afiliados_SS(comunidades)
    plt.tight_layout()
    plt.savefig('images/afiliados.jpeg', dpi=500)
    st.image('images/afiliados.jpeg')

    with st.beta_expander('Conclusiones iniciales Tasa paro y afiliación'):
        st.write('Si observamos por número de afiliados:')
        st.write('Destacan 3 comunidades, Cataluña, Madrid y Andalucia. No obstante si contrastamos con la tasa de '
                 'paro media, en Andalucía la media entre provincias es de mas del 20%, mas de 5 puntos por encima '
                 'que las otras dos comunidades lo que podría significar un menor dinamismo empresarial, '
                 'y un mercadolaboral con menos oportunidades')
        st.write('Si miramos solamente a Tasa de Paro, podemos observar que en las provincias con menor paro, '
                 'tampoco existe un gran número de afiliados a la ss, lo que podria ser un sintoma de estancamiento o '
                 'poca flexibilidad para absorver  a mas trabajadores')
        st.write('En conclusión aunque estamos cruzando unos datos algo genéricos, y requeriria un mayor análisis, '
                 'en este contexto del EDA, no era el punto mas importante. Pudiendo concluir que para la elección de '
                 'donde trabajar en base a estos indicadores necesitaríamos buscar un equilibrio entre un volumen de '
                 'afiliados alto, y una tasa de paro por debajo de la media española. 15,5%')

# Pagina donde analizar el salario en relación al coste de vida
def rendimiento(df,comunidades):
    # -Devuelve compsalario, comparativa del salario medio por comunidad
    # -argumento obligatorio dataframe con los datos generados en exploracion de datos
    # -argumentos opcional, start y stop, para seleccionar un conjunto concreto de provincia. Por defecto todo el conjunto.
    # -argumento opcional, orden, para organizar la salida en funcion de otra columna. Por defecto el salario medio


    def compararsalario(df, start=None, stop=None, orden='Salario Medio'):
        fysize = 6
        if start != None or stop != None:
            fysize = 3
        fig = plt.figure(figsize=(14, fysize), dpi=100)
        ax = fig.gca()
        compsalario = sns.barplot(x='Salario Medio',
                                  y='provincias',
                                  ax=ax,
                                  palette='cool',
                                  data=df.sort_values(by=orden, ascending=False)[start:stop],
                                  ci=None)
        ax.set_ylabel("Comunidad")
        ax.set_xlabel("Salario medio en € y bruto")
        ax.set_title("Salario medio por comunidad")
        show_values_on_bars(compsalario, "h", 0.3)
        return compsalario


    # -Devuelve compcoste, comparativa de los coste de vida
    # -argumento obligatorio dataframe con los datos generados en exploracion de datos
    # -argumentos opcional, start y stop, para seleccionar un conjunto concreto de provincia. Por defecto todo el conjunto.
    # -argumento opcional, orden, para organizar la salida en funcion de otra columna. Por defecto el coste de vida

    def costevida(df, start=None, stop=None, orden='Coste de vida'):
        fysize = 6
        if start != None or stop != None:
            fysize = 3
        fig = plt.figure(figsize=(12, fysize), dpi=100)
        ax = fig.gca()
        compcoste = sns.barplot(x='Coste de vida',
                                y='provincias',
                                ax=ax,
                                palette='cool',
                                data=df.sort_values(by=orden, ascending=False)[start:stop],
                                ci=None)
        ax.set_ylabel("Comunidad")
        ax.set_xlabel("Coste de vida")
        ax.set_title("Coste medio comunidad")
        show_values_on_bars(compcoste, "h", 0.3)
        return compcoste


    # -Devuelve poderad , equiparar salarios en base a la media española.
    # -argumento obligatorio dataframe con los datos generados en exploracion de datos
    # -argumentos opcional, start y stop, para seleccionar un conjunto concreto de provincia. Por defecto todo el conjunto.
    # -argumento opcional, orden, para organizar la salida en funcion de otra columna. Por defecto el salario medio

    comunidades['poder adquisitivo'] = (((100 - comunidades['Coste de vida']) / 100) + 1) * comunidades['Salario Medio']
    comunidades['poder adquisitivo'] = comunidades['poder adquisitivo'].round()

    def poder_adquisitivo(df, start=None, stop=None, orden='poder adquisitivo'):
        fysize = 6
        if start != None or stop != None:
            fysize = 3
        fig = plt.figure(figsize=(14, fysize), dpi=100)
        ax = fig.gca()
        poderad = sns.barplot(x='poder adquisitivo',
                              y='provincias',
                              ax=ax,
                              palette='cool',
                              data=df.sort_values(by=orden, ascending=False)[start:stop],
                              ci=None)
        ax.set_ylabel("Comunidad")
        ax.set_xlabel("Poder adquisisitivo")
        ax.set_title("Poder adquisisitivo en referencia a Coste Vida España")
        show_values_on_bars(poderad, "h", 0.3)
        return poderad


    st.subheader('Rendimiento salario como poder adquisistivo según comunidad')
    st.write('El objetivo es analizar el salario en función del coste de vida')
    checksalario = st.checkbox('Ver salario por comunidades')
    checkscoste = st.checkbox('Ver coste de vida por comunidades')
    checkpoderad = st.checkbox('Ver poder adquisitivo por comunidades')

    if checksalario:
        compararsalario(comunidades)
        plt.tight_layout()
        plt.savefig('images/afiliados.jpeg', dpi=500)
        st.image('images/afiliados.jpeg')
    if checkscoste:
        costevida(comunidades)
        plt.tight_layout()
        plt.savefig('images/coste.jpeg', dpi=500)
        st.image('images/coste.jpeg')
    if checkpoderad:
        poder_adquisitivo(comunidades)
        plt.tight_layout()
        plt.savefig('images/poder.jpeg', dpi=500)
        st.image('images/poder.jpeg')

    with st.beta_expander('Pulse para calcular rendimiento en base a otra comunidad'):
        def trabajas_vives(df, provincia_trabajas, provincia_vives):
            mask1 = df['provincias'] == provincia_trabajas
            mask2 = df['provincias'] == provincia_vives
            modificador = ((df[mask1]['Coste de vida'].iloc[0] - df[mask2]['Coste de vida'].iloc[0]) / 100) + 1
            poder_adquisitivo = df[mask1]['S Medio'].iloc[0] * modificador
            return poder_adquisitivo

        provincias = list(df['provincias'].unique())

        menutv = st.selectbox("Selecciona la provincia para la que trabajas:", provincias)
        menuresi = st.selectbox("Selecciona la provincia en al que resides o quieres residir:", provincias)
        st.write('El salario medio en: ',menutv , 'de', df['S Medio'][df['provincias'] == menutv])
        st.write('Equivale a un poder adquisitivo de :',trabajas_vives(df, menutv, menuresi), 'en ', menuresi)

    with st.beta_expander('Conclusiones:'):
        st.write('Aunque no se ve en las gráficas mostradas, si se consulta los datos usados del INE para calcular el '
                 'salario vemos que la diferencia de la mediana de los salarios por comunidad es muy parecida '
                 'hablamos de un abanico de menos de 50€ brutos.')
        st.write('No obstante el salario medio si que tiene grandes diferencias, esto implica que los mínimos y '
                 'máximos son bastante diferentes por comundiad.')
        st.write('Si añadimos el coste de vida, obtenido a partir de las variables de renta familiar disponible per '
                 'cápita y del coste de la vivienda. Estas dos variables muestran una buena capacidad predictiva para '
                 'las paridades del poder adquisitivo (PPA) subnacionales estimadas por el Bureau of Economic '
                 'Analysis de los Estados Unidos, obtendremos:')
        st.write('Si recordamos el heatmap de correlación, coste de vida y precio de vivienda tiene una correlación '
                 'directa, se confirma al conocer como se calcula el coste de vida')
        st.write('Y si analizamos los salarios en base al coste de vida, vemos que el poder adquisitivo cambia '
                 'radicalmente para algunas comunidades, comunidades como Madrid, pasan a ser la penúltima en poder '
                 'adquisitivo en base a media del coste de vida en España')
        st.write('Para calcular en base del poder adquisitivo, hemos calculado un modificador en base al coste de '
                 'vida en España y multiplicandolo por el salario medio.')

# Pagina donde ver alquiler m2, importe medio vivienda, tamaño medio vivienda, m2 compra
def vivir(df, alquiler):

    st.subheader('Comprativa de precios de alquiler, compra y tamaño medio por comunidades')
    st.write('Objetivo es tener una visión general entre las diferencias territoriales en el entorno inmobiliario')
    reversed_alquiler = alquiler.iloc[::-1]
    provincias = list(df['provincias'].unique())

    # Visualización histórico m2 alquiler  provincia
    def histalquiler(reversed_alquiler, provincia):
        trace1 = go.Scatter(
            x=reversed_alquiler['Meses'],
            y=reversed_alquiler[provincia],
            name='Salario Medio unidad 10',
            mode='lines',
            marker=dict(color='rgba(16, 112, 2, 0.8)'),
            text=reversed_alquiler['Madrid'])
        data = [trace1, ]

        layout = dict(title='Datos grupales provincias',
                      xaxis=dict(title='Provincias', ticklen=5)
                      )
        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig)


    # -Devuelve compalquiler, comparativa en base al precio  del alquiler por m2 por provincia.
    # -argumento obligatorio dataframe con los datos generados en exploracion de datos
    # -argumentos opcional, start y stop, para seleccionar un conjunto concreto de provincia. Por defecto todo el conjunto.
    # -argumento opcional, orden, para organizar la salida en funcion de otra columna. Por defecto  Precio m2 Alquiler

    def compararalquilerm2(df, start=None, stop=None, orden='Precio m2 Alquiler'):
        fysize = 12
        if start != None or stop != None:
            fysize = 5
        fig = plt.figure(figsize=(14, fysize), dpi=100)
        ax = fig.gca()
        compalquiler = sns.barplot(x='Precio m2 Alquiler',
                                   y='provincias',
                                   ax=ax,
                                   palette='cool',
                                   data=df.sort_values(by=orden, ascending=False)[start:stop],
                                   ci=None)
        ax.set_ylabel("Provincia")
        ax.set_xlabel("Precio m2 alquiler")
        ax.set_title("Precio del metro cuadrado de alquiler por provincias")
        show_values_on_bars(compalquiler, "h", 0.3)
        return compalquiler

    # Visualizaciñon conjunta de m2 compra
    def compararcompram2(df, start=None, stop=None, orden='Precio compra m2'):
        fysize = 15
        if start != None or stop != None:
            fysize = 7
        fig = plt.figure(figsize=(fysize, 4), dpi=100)
        ax = fig.gca()
        compm2v = sns.barplot(x='provincias',
                              y='Precio compra m2',
                              ax=ax,
                              palette='cool',
                              data=df.sort_values(by=orden, ascending=False)[start:stop],
                              ci=None)
        ax.set_ylabel("Precio compra m2")
        ax.set_xlabel("Provincia")
        ax.set_title("Precio medio compra m2")
        plt.xticks(rotation=80)
        return compm2v


    # -Devuelve compventas, comparativa del precio medio de compra escriturado
    # -argumento obligatorio dataframe con los datos generados en exploracion de datos
    # -argumentos opcional, start y stop, para seleccionar un conjunto concreto de provincia. Por defecto todo el conjunto.
    # -argumento opcional, orden, para organizar la salida en funcion de otra columna. Por defecto el VM

    def compararcompras(df, start=None, stop=None, orden='VM'):
        fysize = 15
        if start != None or stop != None:
            fysize = 7
        fig = plt.figure(figsize=(fysize, 4), dpi=100)
        ax = fig.gca()
        compventas = sns.barplot(x='provincias',
                                 y='VM',
                                 ax=ax,
                                 palette='cool',
                                 data=df.sort_values(by=orden, ascending=False)[start:stop],
                                 ci=None)
        ax.set_ylabel("Precio medio compra")
        ax.set_xlabel("Provincia")
        ax.set_title("Precio medio de compra escriturada")
        plt.xticks(rotation=80)
        return compventas

    # Tamaño medio vivienda escriturada
    df['Tamaño medio construido'] = (df['VM'] / df['Precio compra m2']).astype(int)

    def comparartam(df):
        trace2 = go.Scatter(
            x=df['provincias'],
            y=df['Tamaño medio construido'],
            name='Tamaño medio construido',
            mode='lines',
            marker=dict(color='rgba(16, 112, 2, 0.8)'),
            text=df['Tamaño medio construido'])
        data = [trace2]

        layout = dict(title='Tamaño medio construido por provincia',
                      xaxis=dict(title='Provincias', ticklen=5)
                      )
        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig)

    checkalquilerm2 = st.sidebar.checkbox('Comparar precio m2 de alquiler vivienda')
    checkcompram2 = st.sidebar.checkbox('Comparar precio m2 de compra vivienda')
    checkcompras = st.sidebar.checkbox('Comparar precio medio escriturado compra vivienda')
    checktam = st.sidebar.checkbox('Comparar tamaño medio vivienda escriturada')

    if checkalquilerm2:
        compararalquilerm2(df)
        plt.tight_layout()
        plt.savefig('images/alquilerm2.jpeg', dpi=500)
        st.image('images/alquilerm2.jpeg')
    if checkcompram2:
        compararcompram2(df)
        plt.tight_layout()
        plt.savefig('images/compram2.jpeg', dpi=500)
        st.image('images/compram2.jpeg')
    if checkcompras:
        compararcompras(df)
        plt.tight_layout()
        plt.savefig('images/compra.jpeg', dpi=500)
        st.image('images/compra.jpeg')
    if checktam:
        comparartam(df)

    with st.beta_expander("Selecciona la provincia que deseas ver:"):
        menuprov = st.selectbox('Provincias :', provincias)
        histalquiler(reversed_alquiler, menuprov)

    with st.beta_expander('Conclusiones:'):
        st.write('Una vez hemos visto como cambia drásticamente el poder adquisitivo según provincia de trabajo y '
                 'provincia de residencia se hace interesante para poder tomar una decisión valorar el mercado '
                 'inmobiliario para el alquiler y/o al compra:')
        st.write('Podemos observar una correlación directa entre el precio/m2 de alquiler y el de precio/m2 compra. '
                 'Por lo que de este punto no tendremos una decisión clara de si alquilar o comprar, y será una '
                 'opción ams personal.')
        st.write('Hemos obtenido el tamaño medio escriturado al calcular el precio medio escriturado y precio m2.'
                 'Tenemos que tener en cuenta 2 puntos, primero las fuentes:')
        st.write('Mientras que el precio de compra escriturado es fuente oficial INE, el precio del m2, la fuente es '
                 'idealista. Idealista calcula sus precios en base al anuncio, no al precio final, de ahi que la '
                 'correlación siendo directa no sea perfecta')
        st.write('La segunda que podemos observar, que el tamaño medio a nivel nacional se mueve entre 75 y 105 m2 '
                 'construidos, con un posible outlier en Cáceres que merece una posble revision en el futuro.')
        st.write('Los datos usados son: precio m2 con última actualización en JUNIO, y datos del INE con misma fecha')

def cuotafija(cap, i, t):
    cuota = cap * (((1 + i) ** t) * i) / (((1 + i) ** t) - 1)
    return cuota

# Cuadro de amortización
def cuadro_amortizacion(cap, t, i, cuota):
    cap_pen = cap
    mes = 1
    cuad_amort = pd.DataFrame(columns= ['Mes', 'Cuota', 'Amortización', 'Pendiente'])

    while mes <= t:
        intereses = (cap_pen * i)
        amortizacion = cuota - intereses
        cap_pen = cap_pen - amortizacion
        cuad_amort = cuad_amort.append({'Mes': mes,
                                        'Cuota': int(cuota),
                                        'Amortización':int(amortizacion),
                                        'Pendiente':int(cap_pen) }, ignore_index=True)
        mes += 1
    return cuad_amort


# Calculadora hipotecaria
def calculadora_hipoteca():
    # Constantes
    AJD = 0
    IVA = 0.1
    IGC = 0.065

    # Variables de Control
    impuesto = 0
    entrada = 0
    interes = 0
    importe_solicitado = 0
    correcto = False

    # Lista de comunidades para menu y selección del key del diccionario
    comunidades = ["Andalucia", "Aragón", "Canarias", "Cantabria", "Castilla y León",
                   "Castilla-La Mancha", "Cataluña", "Ceuta", "Melilla", "Comunidad de Madrid",
                   "Navarra", "Comunidad Valenciana", "Extremadura", "Galicia",
                   "Islas Baleares", "La Rioja", "País Vasco", "Asturias", "Murcia"]

    # Diccionario key = comunidad, primer valor impuesto aplicable en la fórmula,
    #   segundo valor interes general comunidad
    #   tercer valor lista con el valor impositivo especial
    comunidadesdic = {"Andalucia": [0.08, "del 8 al 10%", ["7 % para vivienda habitual de no más de 130.000 €.",
                                                           "3,5% para vivienda habitual de no más de 130.000 € destinada a un menor de 35 años",
                                                           "o de no más de 180.000 € destinada a una persona con discapacidad superior al 33 % o",
                                                           "miembro de una familia numerosa.\n"]],
                      "Aragón": [0.08, "del 8 al 10%", ["Bonificación del 12,5 % por vivienda habitual de no ",
                                                        "más de 100.000 € para menores de 35 años\n",
                                                        "con discapacidad superior al 65% o mujeres víctimas de violencia de género.\n",
                                                        "Bonificación del 50 % por compra de vivienda habitual para familias numerosas.\n"]],
                      "Canarias": [0.065, "del 6.5%", ["5 % para la compra de vivienda habitual.",
                                                       "1 % para la compra de vivienda habitual de: familias numerosas o monoparentales",
                                                       "y personas con discapacidad física.\n20 % de bonificación para menores de 35 años ",
                                                       "y mujeres víctimas de violencia de género.\n"]],
                      "Cantabria": [0.08, "del 8 al 10%", ["5,5 % para vivienda protegida\n",
                                                           "5 % para la compra de vivienda habitual de familias numerosas, menores de 30 años,",
                                                           "personas con minusvalía \n superior al 33 % o viviendas que se vayan a rehabilitar.\n",
                                                           "4 % para la compra de vivienda habitual de personas con minusvalía superior al 65 %."]],
                      "Castilla y León": [0.08, "del 8%",
                                          ["4 % para la compra de vivienda habitual destinada a familia numerosa,",
                                           "adquiriente o familiar\n",
                                           "con discapacidad superior al 65%, primera vivienda de menores de 36 años",
                                           "o vivienda protegida\n",
                                           "si es la primera vivienda de los adquirientes.\n"]],
                      "Castilla-La Mancha": [0.08, "del 8",
                                             ["6 % para la compra de la primera vivienda habitual del",
                                              "contribuyente, siempre que \n",
                                              "no supere los 180.000 € y financie al menos el 50%.\n"]],
                      "Cataluña": [0.1, "del 10 al 11%", ["7 % para viviendas de protección oficial.\n",
                                                          "5 % para familia numerosas, menores de 32 años",
                                                          "o personas con minusvalía superior al 65 %.\n"]],
                      "Ceuta": [0.06, "del 6%", ["50 % de bonificación si el inmueble está situado en Ceuta\n"]],
                      "Melilla": [0.06, "del 6%",
                                  ["50 % de bonificación si el inmueble está situado en Melilla\n"]],
                      "Comunidad de Madrid": [0.06, "del 6%", [
                          "4 % para la compra de una vivienda habitual destinada a familia numerosa.\n",
                          "10 % de bonificación si se trata de la compra de una vivienda habitual.\n"]],
                      "Navarra": [0.06, "del 6%", ["5 % para los primeros 180.303,63 € de una vivienda",
                                                   "habitual destinada para familias de dos o más hijos."]],
                      "Comunidad Valenciana": [0.1, "del 10%", [
                          "8 % para viviendas de protección pública de régimen general o\n primera vivienda",
                          "habitual de menores de 35 años.\n",
                          "4% para viviendas habituales de protección oficial de régimen\n especial, ",
                          "familias numerosas o personas con un grado de \nminusvalía física superior al",
                          "65 % o psíquico superior al 33 %.\n"]],
                      "Extremadura": [0.08, "del 8 al 11%",
                                      ["7 % para viviendas cuyo valor sea inferior a los 122.000 € y la\n",
                                       "suma de las bases imponibles general y del ahorro del\n contribuyente sea inferior",
                                       "a 19.000 € en declaración individual o 24.000 € en declaración conjunta.",
                                       "4 % par viviendas de protección oficial con precio máximo legal\n"]],
                      "Galicia": [0.1, "del 10%", [
                          "7 % para la compra de la vivienda habitual de familias con\n patrimonio inferior a los 200.000 €.\n",
                          "3 % para la compra de la vivienda habitual de personas con\n minusvalía reconocida",
                          "superior al 65 %, familia numerosa con\n patrimonio inferior a los 400.000 € o menores ",
                          "de 36 años con\n patrimonio inferior a los 200.000 €.\n"]],
                      "Islas Baleares": [0.08, "del 8 al 11%",
                                         ["5 % para la compra de la primera vivienda habitual, siempre que\n",
                                          "no supere los 200.000 €.\n"]],
                      "La Rioja": [0.07, "del 7%", ["Tiene tipo reducido del 5 % o el 3% para casos especiales"]],
                      "País Vasco": [0.04, "del 4%",
                                     ["2,50 % para familias numerosas, viviendas de no más de 120 m2\n",
                                      "(o 300m2 de parcela en unifamiliares) y compra de vivienda habitual\n"]],
                      "Asturias": [0.08, "del 8 al 10%", ["3 % para viviendas de protección oficial.\n"]],
                      "Murcia": [0.08, "del 8%", ["4 % para viviendas protegidas de régimen especial.\n",
                                                  "3 % para vivienda habitual de familias numerosas o menores de\n35 años,",
                                                  "siempre que su valor no supere los 300.000 € en el \nprimer caso y 150.000 € en el segundo.\n"]]}

    st.title('Calculadora hipotecaria')
    st.subheader('Rellene el formulario para obtener los siguientes datos:')
    st.write('Información sobre el ahorro necesario para la compra de vivienda, y la diversificación de dicho ahorro entre impuestos, entrada, notaría y gestoría...')
    st.write('Información sobre cuota de la hipoteca, en base a importe solicitado, plazo en años y % de interés fijo')
    st.write('Tabla de amortización')

    # Formulario que recoge los datos necesarios para calcular cuota hipoteca, tabla de amortización
    # Recoge:  val_viv , será el importe de la vivienda sin impuestos
    #          menunuevo, si la vivienda es nueva o de segunda mano, importa para aplicar ITP o IVA
    #          menucomunidad, almacena comunidad para saber que ITP concreto aplicar
    #          menuviv, si la vivienda es priemra o segunda, así calcular si la entrada es del 20% o 30%
    #          intereses , tipo de interes fijo aplicable
    #          tiempo, plazo en años para luego calcular número de cuotas.
    with st.form(key="my_form"):
        val_viv = st.number_input('Introduzca el precio de compra sin impuestos')

        menunuevo = st.selectbox("La vivienda es nueva o de segunda mano", ('', 'Nueva', 'Segunda mano'))
        if menunuevo == 'Nueva':
            impuesto = IVA
            AJD = 0.015

        else:
            menucomunidad = st.selectbox("Seleccione la comunidad de compra:", comunidades)
            impuesto = comunidadesdic[menucomunidad][0]

        menuviv = st.selectbox("Seleccione si es primera vivienda o segunda:",
                               ('', 'Primera vivienda', 'Segunda  vivienda'))
        if menuviv == 'Primera vivienda':
            entrada = 0.2
        elif menuviv == 'Segunda vivienda':
            entrada = 0.3

        importe_solicitado = st.number_input('Que importe desea solicitar?')

        interes = st.number_input(' A que % de intereses quiere el cálculo')
        interes = (interes / 100) / 12

        tiempo = st.slider('A cuantos años quiere la hipoteca?', min_value=1, max_value=30)
        tiempo = tiempo * 12

        submitted = st.form_submit_button("Ver informe")

        # Controla que no se genere el informe  sino has introducido los parámetros principales
        if (val_viv != 0) and (impuesto != 0) and (importe_solicitado != 0) and (interes != 0) and (entrada != 0):
            correcto = True

        # Crea tablas de informe e impresiones por apntalla de datos
        if submitted and correcto:
            ahorro_nec = ((val_viv * entrada) + (val_viv * impuesto) + 2000 + (AJD * val_viv))
            ahorro_necesario = [int(ahorro_nec)]
            entradaviv = [int(val_viv * entrada)]
            impuestoviv = [int(val_viv * impuesto)]
            notaria_gestoria = [2000]
            ajdviv = [int(AJD * val_viv)]
            calculadora = pd.DataFrame({'AHORRO NECESARIO': ahorro_necesario,
                                        'ENTRADA': entradaviv,
                                        'IMPUESTOS': impuestoviv,
                                        'NOTARIA Y GESTORIA': notaria_gestoria})
            if AJD != 0:
                calculadora['AJD'] = ajdviv
            cuota = cuotafija(importe_solicitado, interes, tiempo)
            porcentajesol = (importe_solicitado * 100) / val_viv
            resumenhip = pd.DataFrame(columns=['Precio Compra', 'Importe Hip.', 'Cuota Hip.', 'Nº Cuotas', 'Porcentaje Solicitado %'])
            resumenhip = resumenhip.append({'Precio Compra': val_viv,
                                            'Importe Hip.': importe_solicitado,
                                            'Cuota Hip.': int(cuota),
                                            'Nº Cuotas': tiempo,
                                            'Porcentaje Solicitado %': porcentajesol}, ignore_index=True)
            st.table(resumenhip)
            if menunuevo == 'Nueva':
                impuesto = IVA
                AJD = 0.015
                st.write(
                    "\n El impuesto a pagar es del 10% salvo en canarias 6,5% sobre el valor de compra de la casa")
                st.write(
                    "\n El impuesto del AJD va del 0,5% al 1,5% que es la cuantía mas común, usaremos la comun por simplificar")
            else:
                if menucomunidad != '':
                    st.write("El impuesto es el ITP Impuesto de Transmision Patrimonial.")
                    st.write("En su comunidad:", menucomunidad, "el tipo general es",
                             comunidadesdic[menucomunidad][1])
                    st.write("Con tipos especiales de:")
                    tipo_especial = ""
                    for i in comunidadesdic[menucomunidad][2]:
                        tipo_especial += i
                    st.write(tipo_especial)
            if (importe_solicitado > (val_viv * (1 - entrada))) and (
                    importe_solicitado <= ((val_viv * ((1 - entrada) + 0.1)))):
                st.write("CUIDADO: VA A NECESITAR MAS TASACIÓN QUE VALOR DE COMPRA PARA TENER ALGUNA POSIBILIDAD")
            elif importe_solicitado > (((val_viv * (1 - entrada) + 0.1))) and importe_solicitado <= val_viv:
                st.write("Salvo funcionario o doble garantía hipotecaria es muy dificil que le den su hipoteca\n",
                         "Una doble garantia hipotecaria es un garantia limitada, que se aplica sobre un segundo bien inmueble\n",
                         "que absorve el exceso de financiación requerida")
            elif importe_solicitado == (val_viv * (1 - entrada)):
                st.write('Perfecto, el importe encaja con los topes generales que tienen los bancos')
            elif importe_solicitado < (val_viv * (1 - entrada)):
                st.write("Genial es muy favorable pedir menos que los topes bancarios estandar")
            else:
                st.write("Seguiré con los calculos, pero mas del 100% no dan los bancos")
            st.write('La cuota de su hipoteca es de:', int(cuota), '€/mes aprox')

            st.table(calculadora)
            st.table(cuadro_amortizacion(importe_solicitado, tiempo, interes, cuota))
        else:
            st.warning('Debe completar cada casilla del formulario para poder hacer los cálculos necesarios')

def conclusiones():
    st.title('Conclusiones Finales')
    st.write('Hemos podido valorar, que efectivamente, el teletrabajo puede suponer un potencial ecónomico en las '
             'economías personales pudiendo generar un diferencial de poder económico en base al coste de vida medible.'
            'Lo que conlleva que si la decisión fuese puramente económica nuestro valor de referencia seria salario-'
             'coste de vida.')
    st.write('Si la decisión es por lugar de residencia deseado, por ejemplo  vivir en al costa, valoraríamos  poder '
            'adquisitivo de esas zonas, contrastando con costes de vivienda')
    st.write('No obstante tener en cuenta que por simplificación el ambito usado ha sido comunidad y provincia cuando'
            'si se quiere tomar una decisión más fundamentada, habría que mirar al ambito municipios, dado que en un '
             'ámbito tan grande no deja de ser generico y orientativo, dado que dentro de comundiades existen grandes '
            'diferencias entre los diferentes municipios.')
