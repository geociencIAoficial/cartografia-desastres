import folium
import pandas as pd
import os

# Leer archivo CSV
ruta_csv = r'C:\Users\richa\Documents\cartografia\ayuda_desastres\lluvias_2025\datos\localidades.csv'
df = pd.read_csv(ruta_csv)

# Crear mapa base
mapa = folium.Map(location=[20.3, -97.85], zoom_start=8, tiles='OpenStreetMap')

# Filtrar filas con latitud y longitud válidas
df = df.dropna(subset=['lat', 'lon'])

# Añadir marcadores desde CSV
for _, loc in df.iterrows():
    popup = f"""
    <b>{loc['nombre']}</b><br>
    Municipio: {loc['municipio']}<br>
    Estado: {loc['estado']}<br>
    <b>Necesidad:</b> {loc['necesidad']}<br>
    <b>Problemática:</b> {loc['problematica']}
    """
    color = {
    'alta': 'red',
    'media': 'orange',
    'baja': 'green'
    }.get(str(loc['status']).strip().lower(), 'gray')


    folium.Marker(
        location=[loc['lat'], loc['lon']],
        popup=popup,
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(mapa)

# Título del mapa
titulo_html = """
<div style="
    position: fixed;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    background-color: white;
    width: 600px;
    padding: 10px 20px;
    border: 2px solid grey;
    z-index: 9999;
    font-size: 16px;
    font-weight: bold;
    text-align: center;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
">
Cartografía para la atención a desastres en localidades de los estados de Puebla y Veracruz, México
</div>
"""
mapa.get_root().html.add_child(folium.Element(titulo_html))

# Leyenda del mapa
leyenda_html = """
<div style="
    position: fixed;
    top: 70px;
    right: 20px;
    width: 200px;
    background-color: white;
    border: 2px solid grey;
    z-index: 9999;
    font-size: 14px;
    padding: 12px;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    line-height: 1.6;
">
<b>Nivel de urgencia</b><br>
<i class="fa fa-map-marker fa-2x" style="color:red"></i> Alta<br>
<i class="fa fa-map-marker fa-2x" style="color:orange"></i> Media<br>
<i class="fa fa-map-marker fa-2x" style="color:green"></i> Baja
</div>
"""
mapa.get_root().html.add_child(folium.Element(leyenda_html))

# Guardar mapa
ruta_salida = r'C:\Users\richa\Documents\cartografia\ayuda_desastres\lluvias_2025\mapas'
os.makedirs(ruta_salida, exist_ok=True)
mapa.save(os.path.join(ruta_salida, 'mapa_lluvias_2025.html'))
