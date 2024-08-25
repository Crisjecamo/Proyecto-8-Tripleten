#!/usr/bin/env python
# coding: utf-8

# # Contenido
# 
# * [Objetivos](#objetivos)
# * [Diccionario de Datos](#diccionario)
# * [Introduccion](#introduccion)
# * [Dataframe 1](#dataframe_1)
#     * [1.1 Observacion](#observacion)
# * [Dataframe 2](#dataframe_2)
#     * [2.1 Observacion](#observacion_2)
# * [3 Dataframe 3](#dataframe_3)
#     * [3.1 Observacion](#observacion_3)
# * [5 Analisis de los Datos](#analisis_de_los_datos)
#     * [5.1 Visitas](#visitas)
#         * [5.1.1 ¿Cuántas personas lo usan cada día, semana y mes?](#cplu)
#             * [5.1.1.1 Observacion](#observacion_4)
#         * [5.1.2 ¿Cuántas sesiones hay por día? (Un/a usuario/a puede tener más de una sesión)](#cshd)
#             * [5.1.2.1 Observacion](#observacion_5)
#         * [5.1.3 ¿Cuál es la duración de cada sesión?](#cdcs)
#             * [5.1.3.1 Observacion](#observacion_6)    
#         * [5.1.4 ¿Con qué frecuencia los usuarios y las usuarias regresan? ](#cfur)
#             * [5.1.4.1 Observacion](#observacion_7)
#     * [5.2 Ventas](#ventas)
#         * [5.2.1 ¿Cuándo la gente empieza a comprar?](#cgec)
#             * [5.2.1.1 Observacion](#observacion_8)
#         * [5.2.2 ¿Cuántos pedidos hacen durante un período de tiempo dado?](#cphdptd)
#             * [5.2.2.1 Observacion](#observacion_9)
#         * [5.2.3 ¿Cuál es el tamaño promedio de compra?](#ctpc)
#             * [5.2.3.1 Observacion](#observacion_10)
#         * [5.2.4 ¿Cuánto dinero traen? (LTV)](#cdt)
#             * [5.2.4.1 Observacion](#observacion_11)
#     * [5.3 Marketing](#marketing)
#         * [5.3.1 ¿Cuánto dinero se gastó? (Total/por fuente de adquisición/a lo largo del tiempo)](#cdg)
#             * [5.3.1.1 Observacion](#observacion_12)
#         * [5.3.2 ¿Cuál fue el costo de adquisición de clientes de cada una de las fuentes?](#cfcaccuf)
#             * [5.3.2.1 Observacion](#observacion_13)
#         * [5.3.3 ¿Cuán rentables eran las inversiones? (ROMI)](#crei)
#             * [5.3.3.1 Observacion](#observacion_14)
# * [Conclusion General](#cg)
# * [Recomendaciones](#recomendaciones)

# # Objetivos <a id='objetivos'></a>
# 
# * cómo los clientes usan el servicio;
# 
# 
# 
# * cuándo empiezan a comprar;
# 
# 
# 
# * cuánto dinero aporta cada cliente a la compañía;
# 
# 
# 
# * cuándo los ingresos cubren el costo de adquisición de los clientes.

# # Diccionario de Datos <a id='diccionario'></a>
# 
# La tabla visits (registros del servidor con datos sobre las visitas al sitio web):
# 
#     * Uid: identificador único del usuario;
#     * Device: dispositivo del usuario;
#     * Start Ts: fecha y hora de inicio de la sesión;
#     * End Ts: fecha y hora de término de la sesión;
#     * Source Id: identificador de la fuente de anuncios de la que proviene el usuario.
#     * Todas las fechas de esta tabla están en formato AAAA-MM-DD.
# 
# 
# 
# 
# La tabla orders (datos sobre pedidos):
# 
#     * Uid: identificador único del usuario que realiza un pedido;
#     * Buy Ts: fecha y hora del pedido;
#     * Revenue: ingresos de Y.Afisha de este pedido.
# 
# 
# 
# La tabla costs (datos sobre gastos de marketing):
# 
#     * source_id: identificador de la fuente de anuncios
#     * dt: fecha;
#     * costs: gastos en esta fuente de anuncios en este día.

# # Introduccion <a id='introduccion'></a>
# 
# Y.Afisha, una plataforma de venta de boletos para eventos, ha experimentado un crecimiento significativo en su base de usuarios y ventas. El análisis de datos realizado abarca aspectos cruciales como patrones de visitas, comportamiento de compra, valor del tiempo de vida del cliente (LTV) y retorno de la inversión en marketing (ROMI). Este estudio proporciona insights valiosos para optimizar las operaciones y estrategias de marketing de la empresa.

# In[1]:


import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns


# In[2]:


df1= pd.read_csv('/datasets/visits_log_us.csv')
df2= pd.read_csv('/datasets/orders_log_us.csv')
df3= pd.read_csv('/datasets/costs_us.csv')


# # Dataframe 1 <a id='dataframe_1'></a>

# In[3]:


# Modificamos las columnas a sus formatos correctos

df1['End Ts']= pd.to_datetime(df1['End Ts'])
df1['Start Ts']= pd.to_datetime(df1['Start Ts'])
df1['Device']= df1['Device'].astype('category')
df1['Uid']= df1['Uid'].astype('int')
df1.info()


# In[4]:


# modificamos los nombres de las columnas para que esten correctamente y visualizamos los datos para verificar los datos.

new_columns1 ={
    'Device': 'device',
    'End Ts': 'end_ts',
    'Source Id': 'source_id',
    'Start Ts': 'start_ts',
    'Uid': 'uid'
}
df1.rename(columns = new_columns1, inplace = True)
print(df1.columns)
print()
print(df1.head())


# In[5]:


#Verificamos cuantos datos con el signo negativo tenemos en esta columna

filtered1= df1['uid'].astype(str)
filtered1[filtered1.str.startswith('-')]


# In[6]:


#Utilizamos el metodo abs para eliminar el signo '-'

df1['uid']= df1['uid'].abs()
df1.head()


# # Observacion: <a id='observacion'></a>
# 
# En este dataset pudimos observar datos con el signo de '-' en la columna 'uid' exactamente 179803 datos, por lo que se procedio a eliminar este signo de los codigos de identificacion unica de cada usuario, tambien modificamos los nombres de las columnas para que tuvieran el formato correcto.

# # Dataframe 2 <a id='dataframe_2'></a>

# In[7]:


# Modificamos las columnas a sus formatos correctos

df2['Buy Ts']= pd.to_datetime(df2['Buy Ts'])
df2['Uid']= df2['Uid'].astype('int')
df2.info()


# In[8]:


# modificamos los nombres de las columnas para que esten correctamente y visualizamos los datos para verificar los datos.

new_columns2 ={
    'Buy Ts': 'buy_ts',
    'Revenue': 'revenue',
    'Uid': 'uid',
}
df2.rename(columns = new_columns2, inplace = True)
print(df2.columns)


# In[9]:


#Visualizamos nuestros datos en busqueda de datos atipicos.

df2.head()


# In[10]:


#Verificamos cuantos datos con el signo negativo tenemos en esta columna

filtered2= df2['uid'].astype(str)
filtered2[filtered2.str.startswith('-')]


# In[11]:


#Utilizamos el metodo abs para eliminar el signo '-'

df2['uid']= df2['uid'].abs()
df2.head()


# In[12]:


#Verificamos si tenemos valores 0 y contamos cual es la cantidad de estos valores en nuestros datos.

filtered_0= df2[df2['revenue']== 0]
print(filtered_0.head(10))
print()
print()
print('Cantidad de ceros: ', len(filtered_0))


# In[13]:


#Descartamos estos datos con valores 0

df2= df2[df2['revenue'] != 0]
df2.info()


# # Observacion: <a id='observacion_2'></a>
# 
# en este dataset tambien encontramos datos con el signo '-' en la columna 'uid' se procedio a realizar la modificacion requerida, realizamos las modificaciones de los nombres de las columnas para tenerlos de manera correcta, tambien encontramos datos en la columna 'revenue' con valores '0', 51 valores en los datos, eliminamos estos datos de nuestro Dataframe.

# # Dataframe 3 <a id='dataframe_3'></a>

# In[14]:


df3['dt']= pd.to_datetime(df3['dt'])
df3.info()


# In[15]:


df3.describe()


# # Observacion: <a id='observacion_3'></a>
# 
# en este dataset, simplemente colocamos el formato correcto a la columna dt, pero no encontramos algun otro dato atipico que corregir. utilizamos el metodo describe() para tener una vision un poco mas clara de los datos. la columna source_id simplemente muestra las funtes de donde provienen los clientes. podemos evidenciar que la media se encuenta entre las fuentes 4 y 5 debemos mas adelante indagar mas sobre esto. 
# 
# En la columna costs tenemos por asi decirlo las inversiones que se realizan para atraer cliente mediante estas fuentes, los costos promedio son alrededor de 129 y su costo maximo esta en aproximadamente 1788.

# # Analisis de los Datos <a id='Analisis_de_los_datos'></a>

# # Visitas <a id='visitas'></a>

# In[16]:


# se crean las nuevas columnas con datos por dia, semana, mes y año. 

df1['session_year']  = df1['start_ts'].dt.year
df1['session_month'] = df1['start_ts'].dt.month
df1['session_week']  = df1['start_ts'].dt.week
df1['session_date'] = df1['start_ts'].dt.date

df1.head()


# # ¿Cuántas personas lo usan cada día, semana y mes? <a id='cplu'></a>

# In[17]:


# Se realizan los calculos con las formulas y los metodos necesarios para saber la cantidad de personas que usan la aplicacion.

dau_total = df1.groupby('session_date').agg({'uid': 'nunique'}).mean()
wau_total = df1.groupby(['session_year', 'session_week']).agg({'uid': 'nunique'}).mean()
mau_total = (df1.groupby(['session_year', 'session_month']).agg({'uid': 'nunique'}).mean())

print('Número de usuarios activos diarios (únicos): ', dau_total)
print()
print()
print('Número de usuarios activos semanales: ', wau_total)
print()
print()
print('Número de usuarios activos mensuales: ', mau_total)


# # Observacion: <a id='observacion_4'></a>
# 
# con los datos analizados podemos saber que en promedio una 908 personas lo usan diario, 5716 lo usan semanal y 23228 lo usan mensualmente.

# # ¿Cuántas sesiones hay por día? (Un/a usuario/a puede tener más de una sesión). <a id='cshd'></a>

# In[18]:


# Agrupamos los datos con las columnas year y date para encontar el numero de usuarios unicos

sessions_per_user = df1.groupby(['session_year', 'session_date']).agg(
    {'uid': ['count', 'nunique']}
)

# cambiamos los nombres de las columnas 

sessions_per_user.columns = ['n_sessions', 'n_users']

# Encontramos la cantidad de sesiones por usuario diario

sessions_per_user['sessions_per_user'] = (
    sessions_per_user['n_sessions'] / sessions_per_user['n_users']
)
sessions_per_user= sessions_per_user.reset_index()
print(sessions_per_user)


# In[19]:


# se grafica un histograma para observar la distribución del número de sesiones por usuario para cada día

sessions_per_user['sessions_per_user'].plot(kind= 'hist',
                                        bins= 100,
                                       title= 'Número de sesiones por usuario',
                                       figsize= (12, 8),
                                       color= 'darkcyan'
                                       )
plt.xlabel('Número de Sesiones por Día')
plt.ylabel('Frecuencia')
plt.show()


# In[20]:


# Se grafica los pedidos totales para cada mes donde se efectuo la compra
sessions_per_user.plot(x = 'session_date',
                  y= 'sessions_per_user',
                  kind= 'line',
                  figsize= [12,8],
                  fontsize= 12,
                  rot= 90,
                  color= 'darkcyan',
                  legend=False     
                       )
plt.title('Numero de sesiones por usuarios mensuales', fontsize=15)
plt.xlabel('Mes', fontsize=15)
plt.ylabel('Cantidad promedio de sesiones', fontsize=15)


plt.show()


# # Observacion: <a id='observacion_5'></a>
# 
# Podemos visualizar en el histograma que normalmente el numero de sesiones por usuario por dia es 1 en promedio. En nuestro nuevo grafico se puede evidenciar que en el mes de diciembre la cantidad de sesiones es mayor que el resto de los meses y vemos tambien una caida en el mes de abril.

# # ¿Cuál es la duración de cada sesión? <a id='cdcs'></a>

# In[21]:


# creamos una nueva columna session_duration_sec y restamos end_ts y start_ts para encontar la duracion
# visualizamos la media y creamos un histograma para visualizar los datos
# por ultimo dado que los datos no son normales se calcula la moda

df1['session_duration_sec'] = (df1['end_ts'] - df1['start_ts']).dt.seconds
print(df1['session_duration_sec'].mean())
df1['session_duration_sec'].hist(bins=100)
asl= df1['session_duration_sec'].mode()
print(asl)


# In[22]:


# Utilizamos el metodo describe() para tener una idea mas clara sobre los datos de esta columna

df1['session_duration_sec'].describe()


# # Observacion: <a id='observacion_6'></a>
# 
# En este analisis pudimos observar que tenemos datos atipicos, el valor maximo de duracion que tenemos registrado es de 84480 segundos, 1408 minutos unas 24 horas aproximadamente o un dia completo por esa razon decidimos calcular la moda, lo cual nos arrojo que la duracion promedio de un usuario es de 60 segundos o 1 minito.

# # ¿Con qué frecuencia los usuarios y las usuarias regresan? <a id='cfur'></a>

# In[23]:


# realizamos los calculos con sticky para calcular la frecuencia.

sticky_wau= dau_total/wau_total * 100
print(sticky_wau)
sticky_mau= dau_total/mau_total * 100
print(sticky_mau)


# # Observacion: <a id='observacion_7'></a>
# 
# * sticky_wau = 18.512582: Esto significa que aproximadamente el 18.51 % de los usuarios que usan la plataforma en una semana también la usan diariamente.
# 
# 
# 
# 
# * sticky_mau = 6.040741: Esto significa que aproximadamente el 6.04 % de los usuarios que usan la plataforma en un mes también la usan diariamente.
# 
# 
# 
# 
# * Compromiso diario: el porcentaje de usuarios activos diarios sobre usuarios semanales es relativamente alto (18,51 %). Esto sugiere que una parte considerable de los usuarios interactúan con la plataforma a diario, lo que indica un buen nivel de retención en el corto plazo.
# 
# 
# 
# 
# * Desafíos en la retención a largo plazo: el porcentaje de usuarios activos diarios en relación con los usuarios mensuales es significativamente menor (6,04 %). Esto puede indicar que, si bien la plataforma logra atraer usuarios y mantenerlos interesados en el corto plazo, existe un desafío para convertir a estos usuarios en usuarios activos en el largo plazo.
# 

# # Ventas <a id='ventas'></a>

# In[24]:


df2.head()


# # ¿Cuándo la gente empieza a comprar? <a id='cgec'></a>

# In[25]:


# agregar columna de mes de inicio de sesión en DataFrame 'df1'
# y en el DataFrame 'df2' la columna de mes de pedido
df1['month_session'] = df1['start_ts'].astype('datetime64[M]')
df2['order_month'] = df2['buy_ts'].astype('datetime64[M]')


# In[26]:


# se busca la primer sesión para cada usuario
first_session_dates = df1.groupby('uid')['month_session'].min().reset_index()
# se cambia el nombre de la columna 
first_session_dates.columns = ['uid', 'first_session_month']
first_session_dates.head()


# In[27]:


# se une al DataFrame 'df1' con merge
visits_log_us_ = df1.merge(first_session_dates, on= 'uid')
visits_log_us_.head(3)


# In[28]:


# se busca la fecha para la primera orden para cada usuario
first_buy_dates = df2.groupby('uid')['order_month'].min().reset_index()
# se cambia el nombre de la columna 
first_buy_dates.columns = ['uid', 'first_buy_month']
first_buy_dates.head()


# In[29]:


# se una al DataFrame 'df2' con merge
orders_log_us_ = df2.merge(first_buy_dates, on= 'uid')
orders_log_us_.head(3)


# In[30]:


# se unen los DataFrame 'visits_log_us_' con 'orders_log_us_'
visits_orders = visits_log_us_.merge(orders_log_us_, on= 'uid')
visits_orders.head(3)


# In[31]:


# se calcula los días trancurridos cuando el/la usuario/a se convierte en cliente
visits_orders['convertion_time_days'] = (visits_orders['first_buy_month'] - visits_orders['first_session_month']).dt.days
visits_orders.head(3)


# In[32]:


# se categoriza el tiempo de conversión
bins = [-1, 0, 1, 7, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]  # Definir los intervalos 
labels = ['Conversion 0d', 'Conversion 1d', 'Conversion 1w', 'Conversion 1m', 'Conversion 2m', 'Conversion 3m', 'Conversion 4m', 'Conversion 5m', 'Conversion 6m', 'Conversion 7m', 'Conversion 8m', 'Conversion 9m', 'Conversion 10m', 'Conversion 11m', 'Conversion 12m']
visits_orders['conversion_category'] = pd.cut(visits_orders['convertion_time_days'], bins=bins, labels=labels)
# se imprime una muestra de filas
visits_orders.sample(5)


# In[33]:


# ahora se crea una tabla dinámica para saber la cantidad de pedidos que hicieron los usuarios por cohorte (que son los que 
# se registracion por primera vez) y el tiempo que tardaron en hacer su primer pedido 'conversion_category'
first_session_cohort = visits_orders.pivot_table(index= 'first_session_month',
                                       columns= 'conversion_category',
                                       values= 'uid',
                                       aggfunc= 'nunique')


# In[34]:


# se grafica un mapa de calor a partir de first_session_cohort
plt.figure(figsize=(18, 9))

sns.heatmap(first_session_cohort, annot=True, fmt='g', cmap="crest", linewidths= 1, linecolor='black')

plt.title('Cantidad de Usuarios por Primer Pedido', fontsize= 16)
plt.xlabel('Categoría de conversión', fontsize= 14)


plt.show()


# <div class="alert alert-block alert-success">
# <b>Comentario del revisor (1ra Iteracion)</b> <a class=“tocSkip”></a>
# 
# Muy buen trabajo! Con esta visualización es super claro identificar diferencias
# </div>

# In[35]:


#Realizamos la suma por categoria de conversion para obtener la cantidad total
first_session_cohort.sum(axis=0)


# In[36]:


# Ahora las cohortes se definen por el periodo de tiempo de conversión
# se emplea una tabla dinámica para saber la cantidad de pedidos que hicieron de acuerdo a la fuente del anuncio
convertion_time_cohort = visits_orders.pivot_table(index= 'conversion_category',
                             columns= 'source_id',
                             values= 'uid',
                             aggfunc= 'nunique')


# In[37]:


# se grafica un mapa de calor a partir de convertion_time_cohort
plt.figure(figsize=(18, 9))

sns.heatmap(convertion_time_cohort, annot=True, fmt='g', cmap="crest",  linewidths= 1, linecolor='black')

plt.title('', fontsize= 16)
plt.xlabel('Fuente de anuncios de la que proviene el usuario', fontsize= 14)


plt.show()


# In[38]:


# Realizamos la sum por fuente de anuncios para visualizar que fuente genera mayores usuarios
convertion_time_cohort.sum(axis=0)


# # Observacion: <a id='observacion_8'></a>
# 
# Por lo general nuestros usuarios en su gran mayoria compran el primer dia en el que visitan nuestra aplicacion o pagina web tenemos en total unos 30073 usuarios que compraron desde su primera visita, luego podemos notar alrededor de 3000 usuarios que se decidieron compran luego de 1, 2 o 3 meses de haber visitado nuestra pagina web o aplicacion. 
# 
# Tambien analizamos las fuentes de donde provienen nuestros clientes para determinar cuales estan siendo mas efectivas y pudimos notar que las fuentes 3, 4 y 5 son las que nos estan generando mayores usuarios de 10000 a 14000, las fuentes 1 y 2 son los que tambien estan generando un flujo aceptable de usuarios de 7000 a 7300, las fuentes 9 y 10 si estan generando usuarios de 1700 a 2800, pero no con tan alto flujo como las anteriores  y por ultimo tenemos la fuente 7 la cual no esta generando absolutamente ningun usuario apenas solo 1, por lo que deberiamos descartarla.

# # ¿Cuántos pedidos hacen durante un período de tiempo dado? <a id='cphdptd'></a>

# In[39]:


#agrupamos los datos por order_month y aplicamos el parametro count y buscamos los uid unicos con el metodo agg
order_per_month= orders_log_us_.groupby(['order_month'])['uid'].agg(['count', 'nunique']).reset_index()
# cambiamos los nombres de las columnas
order_per_month.columns= ['order_month', 'n_order', 'n_users']
order_per_month


# In[40]:


# calculamos las cantidad de ordenes por usuario mensuales
order_per_month['order_per_user']= order_per_month['n_order'] / order_per_month['n_users']


# In[41]:


order_per_month


# In[42]:


# Se grafica los pedidos totales para cada mes donde se efectuo la compra
order_per_month.plot(x = 'order_month',
                  y= 'n_order',
                  kind= 'line',
                  figsize= [12,8],
                  fontsize= 12,
                  rot= 90,
                  color= 'darkcyan'
                       )
plt.title('Pedidos de los Usuarios por Mes', fontsize=15)
plt.xlabel('Mes del Pedido', fontsize=15)
plt.ylabel('Cantidad Total de Pedidos', fontsize=15)


plt.show()


# # Observacion: <a id='observacion_9'></a>
# 
# En este estudios de analisis de la cantidad de pedidos realizados por los usuarios mensualmente. podemos notar que las mejores ventas se presentaron desde octubre de 2017 a marzo de 2018. con cantidades de pedidos que van desde los 5000 mil hasta un poco mas de los 6000.

# # ¿Cuál es el tamaño promedio de compra? <a id='ctpc'></a>

# In[43]:


# Se calcula el promedio de los pedidos y el promedio de pedidos por usuario/a 
total_orders_mean = order_per_month['n_order'].mean().round()
orders_per_user_mean = order_per_month['order_per_user'].mean().round()
print(f'El promedio de pedidos que se hacen mensual es de {total_orders_mean}')
print(f'Los pedidos en promedio que se hacen por usuario/a mensual son de {orders_per_user_mean}')


# # Observacion: <a id='observacion_10'></a>
# 
# El tamaño promedio de compra total mensual es de 3874 pedidos mensuales y el promedio de pedidos por usuario mensual es de 1 pedido mensual.

# # ¿Cuánto dinero traen? (LTV) <a id='cdt'></a>

# In[44]:


cohort_sizes = orders_log_us_.groupby('first_buy_month').agg({'uid': 'nunique'}).reset_index()
cohort_sizes.columns = ['first_buy_month', 'n_buyers']
cohort_sizes.head()


# In[45]:


cohorts = orders_log_us_.groupby(['first_buy_month','order_month']).agg({'revenue': 'sum'}).reset_index()
cohorts.head()


# In[46]:


report = pd.merge(cohort_sizes, cohorts, on='first_buy_month')
report.head()


# In[47]:


report['age'] = (
    report['order_month'] - report['first_buy_month']
) / np.timedelta64(1, 'M')
report['age'] = report['age'].round().astype('int')

report['ltv'] = report['revenue'] / report['n_buyers']

report.head()


# In[48]:


output = report.pivot_table(
    index='first_buy_month', columns='age', values='ltv', aggfunc='mean'
)

output.fillna('')


# In[49]:


# se grafica un mapa de calor a partir de output
plt.figure(figsize=(18, 9))

sns.heatmap(output, annot=True, fmt='.2f', cmap="crest",  linewidths= 1, linecolor='black')

plt.title('LTV promedio de los/las Clientes.', fontsize= 16)
plt.xlabel('Edad de la Cohorte', fontsize= 14)


plt.show()


# <div class="alert alert-block alert-success">
# <b>Comentario del revisor (2da Iteracion)</b> <a class=“tocSkip”></a>
# 
# Buen trabajo con la corrección!
# </div>

# In[50]:


output.sum(axis=1).round()


# # 
# 

# # Observacion: <a id='observacion_11'></a>
# 
# Podemos evidenciar nuevamente que los mayores ingresos se generan desde la edad de cohorte 0, esto nos confirma que la moryoria de nuestros clientes compran en su primera visita. los mejores ingresos los tenemos en el cohoter de junio y el cohorte de septiembre luego los demas cohortes se mantienen en un estandar de entre 4 y 7 excepto junio de 2018 que si esta en 3 pero esto pudiera estar generandose devido a que no estan todos los registros de este mes.

# # Marketing <a id='marketing'></a>

# In[51]:


df3.head()


# # ¿Cuánto dinero se gastó? (Total/por fuente de adquisición/a lo largo del tiempo) <a id='cdg'></a>

# In[52]:


report_ = pd.merge(report, df3, left_on='order_month', right_on='dt')
report_['cac'] = report_['costs'] / report_['n_buyers']
report_.head()


# In[53]:


# Se agrupa el total de los costos de marketing a lo largo del tiempo
source_costs = report_.groupby('dt')['costs'].sum().sort_values(ascending= False)
source_costs


# In[54]:


# se grafican los costos totales a los largo del tiempo
source_costs.plot(
                  kind= 'line',
                  figsize= [12,8],
                  fontsize= 12,
                  color= 'darkblue'
                       )
plt.title('Costos Totales a lo largo del tiempo', fontsize=15)
plt.xlabel('Fecha', fontsize=15)
plt.ylabel('Cantidad Total de Costos', fontsize=15)

plt.show()


# # Observacion: <a id='observacion_12'></a>
# 
# Los meses con mayores costos fueron Febrero de 2018 con (12409) y Marzo de 2018 con (14373), luego el mes 4 y 5 se redujo a los costos por asi decirlo estandar que se venian veniendo desde meses anteriores los cuales son costos no mayores a 7500.

# # ¿Cuál fue el costo de adquisición de clientes de cada una de las fuentes? <a id='cfcaccuf'></a>

# In[55]:


# se agrupan la suma del costo de adquisición por la fuente del anuncio
cac_by_source = report_.groupby('source_id')['cac'].sum()
cac_by_source


# In[56]:


# se grafican el cac por fuente del anuncio
cac_by_source.plot(
                  kind= 'bar',
                  figsize= [10,6],
                  fontsize= 12,
                  rot= 0,
                  color= 'darkblue'
                       )
plt.title('Costo de Adquisición por Fuente del Anuncio', fontsize=15)
plt.xlabel('Fuente del Anuncio', fontsize=15)
plt.ylabel('Costo de Adquisición', fontsize=15)

plt.show()


# # Observacion: <a id='observacion_13'></a>
# 
# Nuestros análisis previos identificaron a las fuentes 3 y 4 como las principales generadoras de clientes, destacando la fuente 4 por su mayor volumen de usuarios. Sin embargo, el nuevo análisis revela que, aunque la fuente 3 también contribuye, su costo por usuario es aproximadamente tres veces superior al de la fuente 4.
# 
# En conclusión, la fuente 4 se posiciona como la más efectiva tanto por su rentabilidad como por su capacidad de atracción. Proponemos un análisis más profundo de las estrategias implementadas en la fuente 4 para evaluar su replicabilidad en las demás fuentes. Especialmente, en la fuente 3 se debe priorizar la optimización de su costo de adquisición. 

# # ¿Cuán rentables eran las inversiones? (ROMI) <a id='crei'></a>

# In[57]:


report_['romi'] = report_['ltv'] / report_['cac']
output2 = report_.pivot_table(
    index='first_buy_month', columns='age', values='romi', aggfunc='mean'
).round()

output2.fillna('')


# In[58]:


# se grafica un mapa de calor a partir de result_romi
plt.figure(figsize=(16, 9))

sns.heatmap(output2, annot=True, fmt='0.0f', cmap="crest",  linewidths= 1, linecolor='black')

plt.title('Rentabilidad de las inversiones (ROMI).', fontsize= 16)
plt.xlabel('Edad de la Cohorte', fontsize= 14)


plt.show()


# <div class="alert alert-block alert-success">
# <b>Comentario del revisor (1ra Iteracion)</b> <a class=“tocSkip”></a>
# 
# Buen trabajo con esta visualización y cálculo!
# </div>

# In[59]:


output3 = report_.pivot_table(
    index='first_buy_month', columns='age', values='romi', aggfunc='mean'
).round().cumsum(axis=1)


output3.fillna('')


# In[60]:


#se grafica un mapa de calor a partir de output3
plt.figure(figsize=(16, 9))

sns.heatmap(output3, annot=True, fmt='.1f', cmap="crest",  linewidths= 1, linecolor='black')

plt.title('Rentabilidad acunulativa por cohorte de las inversiones (ROMI)', fontsize= 16)
plt.xlabel('Edad de la Cohorte', fontsize= 14)


plt.show()


# <div class="alert alert-block alert-success">
# <b>Comentario del revisor (2da Iteracion)</b> <a class=“tocSkip”></a>
# 
# Buen trabajo con la corrección!
# </div>

# In[61]:


output3.cumsum(axis=1).mean(axis=0).round()


# In[62]:


favorite_platform= df1['device'].value_counts().reset_index()
favorite_platform.columns= ['platform', 'count']
favorite_platform['%']= ((favorite_platform['count'] * 100) / 359400).round() 
favorite_platform


# In[63]:


# se grafican el cac por fuente del anuncio
favorite_platform.plot(
                  kind= 'bar',
                  x= 'platform',
                  figsize= [10,6],
                  fontsize= 12,
                  rot= 0,
                  color= 'darkblue',
                  legend= False
                       )
plt.title('Plataforma preferida por los usuarios', fontsize=15)
plt.xlabel('Plataformas', fontsize=15)
plt.ylabel('Cantidad de visitas', fontsize=15)

plt.show()


# # Observacion: <a id='observacion_14'></a>
# 
# El análisis de las cohortes revela que el costo de adquisición de cada usuario se recupera rápidamente, generando un margen de beneficio promedio entre 400 y 900 mensuales. Este resultado es altamente positivo, dado el bajo costo de adquisición.
# 
# Respecto a los dispositivos utilizados, observamos una clara preferencia por las computadoras de escritorio, con un 73% del tráfico total. Los dispositivos móviles representan el 27% restante. Estos datos sugieren que podríamos explorar estrategias de optimización para dispositivos móviles a fin de aumentar su contribución a los ingresos.

# # Conclusion General <a id='cg'></a>
# 
# ## Visitas
# 
# ### ¿Cuántas personas lo usan cada día, semana y mes?
# 
# * Número de usuarios activos diarios (únicos):  908
# 
# 
# * Número de usuarios activos semanales:  5716
# 
# 
# * Número de usuarios activos mensuales:   23228
# 
# Con los datos analizados podemos saber que en promedio una 908 personas lo usan diario, 5716 lo usan semanal y 23228 lo usan mensualmente.
# 
# ### ¿Cuántas sesiones hay por día? (Un/a usuario/a puede tener más de una sesión)
# 
# ![Screenshot_3.jpg](attachment:Screenshot_3.jpg)

# ![Screenshot_2.jpg](attachment:Screenshot_2.jpg)
# 
# Podemos visualizar en el histograma que normalmente el numero de sesiones por usuario por dia es 1 en promedio. En nuestro nuevo grafico se puede evidenciar que en el mes de diciembre la cantidad de sesiones es mayor que el resto de los meses y vemos tambien una caida en el mes de abril.

# ### ¿Cuál es la duración de cada sesión?
# 
# ![Screenshot_4.jpg](attachment:Screenshot_4.jpg)
# 
# En este analisis pudimos observar que tenemos datos atipicos, el valor maximo de duracion que tenemos registrado es de 84480 segundos, 1408 minutos unas 24 horas aproximadamente o un dia completo por esa razon decidimos calcular la moda, lo cual nos arrojo que la duracion promedio de un usuario es de 60 segundos o 1 minito.

# ###  ¿Con qué frecuencia los usuarios y las usuarias regresan?
# 
# * sticky_wau = 18.512582: Esto significa que aproximadamente el 18.51 % de los usuarios que usan la plataforma en una semana también la usan diariamente.
# 
# 
# 
# 
# * sticky_mau = 6.040741: Esto significa que aproximadamente el 6.04 % de los usuarios que usan la plataforma en un mes también la usan diariamente.
# 
# 
# 
# 
# * Compromiso diario: el porcentaje de usuarios activos diarios sobre usuarios semanales es relativamente alto (18,51 %). Esto sugiere que una parte considerable de los usuarios interactúan con la plataforma a diario, lo que indica un buen nivel de retención en el corto plazo.
# 
# 
# 
# 
# * Desafíos en la retención a largo plazo: el porcentaje de usuarios activos diarios en relación con los usuarios mensuales es significativamente menor (6,04 %). Esto puede indicar que, si bien la plataforma logra atraer usuarios y mantenerlos interesados en el corto plazo, existe un desafío para convertir a estos usuarios en usuarios activos en el largo plazo.
# 
# ## Ventas
# 
# ### ¿Cuándo la gente empieza a comprar?
# 
# ![Screenshot_5.jpg](attachment:Screenshot_5.jpg)
# 
# conversion_category
# 
# * Conversion 0d: 30073
# 
# * Conversion 1d:  0
# 
# * Conversion 1w:  0
# 
# * Conversion 1m: 1158
# 
# * Conversion 2m:      1317
# 
# * Conversion 3m:      1135
# 
# * Conversion 4m:       792
# 
# * Conversion 5m:       476
# 
# * Conversion 6m:       513
# 
# * Conversion 7m:       370
# 
# * Conversion 8m:       259
# 
# * Conversion 9m:       181
# 
# * Conversion 10m:      122
# 
# * Conversion 11m:       59
# 
# * Conversion 12m:       54

# ![Screenshot_6.jpg](attachment:Screenshot_6.jpg)
# 
# source_id
# 
# * 1:      7133
# * 2:      7302
# * 3:     13839
# * 4:     14250
# * 5:     10154
# * 7:         1
# * 9:      2792
# * 10:     1770
# 
# 
# Por lo general nuestros usuarios en su gran mayoria compran el primer dia en el que visitan nuestra aplicacion o pagina web tenemos en total unos 30073 usuarios que compraron desde su primera visita, luego podemos notar alrededor de 3000 usuarios que se decidieron compran luego de 1, 2 o 3 meses de haber visitado nuestra pagina web o aplicacion.
# 
# Tambien analizamos las fuentes de donde provienen nuestros clientes para determinar cuales estan siendo mas efectivas y pudimos notar que las fuentes 3, 4 y 5 son las que nos estan generando mayores usuarios de 10000 a 14000, las fuentes 1 y 2 son los que tambien estan generando un flujo aceptable de usuarios de 7000 a 7300, las fuentes 9 y 10 si estan generando usuarios de 1700 a 2800, pero no con tan alto flujo como las anteriores y por ultimo tenemos la fuente 7 la cual no esta generando absolutamente ningun usuario apenas solo 1, por lo que deberiamos descartarla.

# ### ¿Cuántos pedidos hacen durante un período de tiempo dado?
# 
# ![Screenshot_7.jpg](attachment:Screenshot_7.jpg)
# 
# En este estudios de analisis de la cantidad de pedidos realizados por los usuarios mensualmente. podemos notar que las mejores ventas se presentaron desde octubre de 2017 a marzo de 2018. con cantidades de pedidos que van desde los 5000 mil hasta un poco mas de los 6000.

# ### ¿Cuál es el tamaño promedio de compra?
# 
# * El promedio de pedidos que se hacen mensual es de 3874.0
# 
# 
# 
# * Los pedidos en promedio que se hacen por usuario/a mensual son de 1.0
# 
# El tamaño promedio de compra total mensual es de 3874 pedidos mensuales y el promedio de pedidos por usuario mensual es de 1 pedido mensual.

# ### ¿Cuánto dinero traen? (LTV)
# 
# ![Screenshot_3.jpg](attachment:Screenshot_3.jpg)
# 
# first_buy_month
# 
# * 2017-06-01    12.0
# * 2017-07-01:     8.0
# * 2017-08-01:     8.0
# * 2017-09-01:    13.0
# * 2017-10-01:     6.0
# * 2017-11-01:     6.0
# * 2017-12-01:     8.0
# * 2018-01-01:     5.0
# * 2018-02-01:     5.0
# * 2018-03-01:     5.0
# * 2018-04-01:     5.0
# * 2018-05-01:     5.0
# * 2018-06-01:     3.0
# 
# Podemos evidenciar nuevamente que los mayores ingresos se generan desde la edad de cohorte 0, esto nos confirma que la moryoria de nuestros clientes compran en su primera visita. los mejores ingresos los tenemos en el cohoter de junio y el cohorte de septiembre luego los demas cohortes se mantienen en un estandar de entre 5 y 8 excepto junio de 2018 que si esta en 3 pero esto pudiera estar generandose devido a que no estan todos los registros de este mes.

# ## Marketing
# 
# ### ¿Cuánto dinero se gastó? (Total/por fuente de adquisición/a lo largo del tiempo)
# 
# ![Screenshot_9.jpg](attachment:Screenshot_9.jpg)
# 
# dt
# 
# * 2018-03-01:    14372.80
# * 2018-02-01:    12408.84
# * 2017-12-01:     7435.05
# * 2017-11-01:     7418.46
# * 2018-05-01:     7164.72
# * 2018-01-01:     6868.72
# * 2017-10-01:     5186.20
# * 2017-09-01:     2155.04
# * 2017-08-01:     1526.97
# * 2017-07-01:      756.08
# * 2017-06-01:      735.26
# 
# Los meses con mayores costos fueron Febrero de 2018 con (12409) y Marzo de 2018 con (14373), luego el mes 4 y 5 se redujo a los costos por asi decirlo estandar que se venian veniendo desde meses anteriores los cuales son costos no mayores a 7500.

# ### ¿Cuál fue el costo de adquisición de clientes de cada una de las fuentes?
# 
# ![Screenshot_10.jpg](attachment:Screenshot_10.jpg)
# 
# source_id
# * 1:      1.669532
# * 2:      3.520368
# * 3:     12.475347
# * 4:      3.716047
# * 5:      4.504085
# * 9:      0.512617
# * 10:     0.435294
# 
# Nuestros análisis previos identificaron a las fuentes 3 y 4 como las principales generadoras de clientes, destacando la fuente 4 por su mayor volumen de usuarios. Sin embargo, el nuevo análisis revela que, aunque la fuente 3 también contribuye, su costo por usuario es aproximadamente tres veces superior al de la fuente 4.
# 
# En conclusión, la fuente 4 se posiciona como la más efectiva tanto por su rentabilidad como por su capacidad de atracción. Proponemos un análisis más profundo de las estrategias implementadas en la fuente 4 para evaluar su replicabilidad en las demás fuentes. Especialmente, en la fuente 3 se debe priorizar la optimización de su costo de adquisición.

# ![Screenshot_12.jpg](attachment:Screenshot_12.jpg)
# 
# age
# 
# * 0:     471.0
# * 1:     447.0
# * 2:     540.0
# * 3:     621.0
# * 4:     606.0
# * 5:     722.0
# * 6:     685.0
# * 7:     668.0
# * 8:     862.0
# * 9:     548.0
# * 10:    900.0
# * 11:    687.0

# ![Screenshot_14.jpg](attachment:Screenshot_14.jpg)
# 
# El análisis de las cohortes revela que el costo de adquisición de cada usuario se recupera rápidamente, generando un margen de beneficio promedio entre 400 y 900 mensuales. Este resultado es altamente positivo, dado el bajo costo de adquisición.
# 
# Respecto a los dispositivos utilizados, observamos una clara preferencia por las computadoras de escritorio, con un 73% del tráfico total. Los dispositivos móviles representan el 27% restante. Estos datos sugieren que podríamos explorar estrategias de optimización para dispositivos móviles a fin de aumentar su contribución a los ingresos.

# # Recomendaciones <a id='recomendaciones'></a>
# 
# 
# ## Optimización de la Experiencia de Usuario:
# 
#     * Dado que la mayoría de las compras ocurren el primer día de visita, enfócarse en mejorar la experiencia de usuario inicial para aumentar las conversiones.
#     
#     * Considerar implementar estrategias de retención para aumentar el porcentaje de usuarios activos diarios, especialmente a largo plazo.
# 
# 
# ## Estrategia de Marketing Multicanal:
# 
#     * Priorizar la inversión en las fuentes de adquisición 3 y 4, que han demostrado ser las más efectivas en términos de volumen de usuarios.
#     
#     * Optimizar las estrategias para la fuente 3 para reducir su costo de adquisición de clientes, que actualmente es tres veces superior al de la fuente 4.
#     
#     * Considerar reducir o eliminar la inversión en la fuente 7, que ha demostrado ser ineficaz.
# 
# 
# ## Optimización para Dispositivos Móviles:
# 
#     * Aunque las computadoras de escritorio dominan con un 73% del tráfico, recomiendo invertir en mejorar la experiencia móvil para capturar una mayor parte del 27% del tráfico móvil.
#     
#     * Desarrollar estrategias específicas para aumentar las conversiones en dispositivos móviles.
# 
# 
# ## Segmentación y Personalización:
# 
#     * Utilizar los datos de cohortes para personalizar las ofertas y comunicaciones basadas en el comportamiento de compra de los usuarios.
#     
#     * Implementar estrategias de reactivación para usuarios que no han realizado compras después de su visita inicial.
# 
# 
# ## Gestión del Ciclo de Vida del Cliente:
# 
#     * Desarrollar programas de fidelización para aumentar la frecuencia de compra, ya que el promedio actual es de 1 pedido mensual por usuario.
#     
#     * Implementar estrategias para aumentar el valor de compra promedio y, por ende, el LTV de los clientes.
# 
# 
# ## Optimización de Costos de Marketing:
# 
#     * Continúar monitoreando y optimizando el ROMI, que actualmente muestra un rendimiento positivo con márgenes de beneficio entre 400 y 900 mensuales por usuario.
#     
#     * Considerar redistribuir el presupuesto de marketing hacia las fuentes con mejor rendimiento y menor costo de adquisición.
# 
# 
# ## Análisis Continuo y Toma de Decisiones Basada en Datos:
# 
#     * Establecer un sistema de monitoreo continuo de KPIs clave como DAU, WAU, MAU, tasa de conversión, y ROMI.
#     
#     * Utilizar estos datos para informar decisiones estratégicas y ajustar las tácticas de marketing y desarrollo de producto.
# 
# 
# 
# Implementando estas recomendaciones, Y.Afisha puede optimizar su rendimiento, mejorar la experiencia del usuario y maximizar el retorno de sus inversiones en marketing, asegurando un crecimiento sostenible y rentable a largo plazo.

# <div class="alert alert-block alert-info">
# <b>Comentario general (1ra Iteracion)</b> <a class=“tocSkip”></a>
# 
# Muy bien hecho Cristhoper! De manera general puedo decirte que presentaste un proyecto muy completo, revisaste minusiosamente cada punto de interés para este caso de análisis lo cual demuestra tu capacidad análitica y sobre todo en cómo te apoyas en datos para poder generar las conclusiones acertadas. 
#     
# Te felicito por como redactaste la parte final dando recomendaciones para los próximos pasos a realizar, parte de un análsis es ayudar a la toma de decisiones basadas en datos.
#     
# Saludos!
# </div>
