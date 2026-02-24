import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

# Archivo seguro de la clave
ARCHIVO_CLAVE = r"C:\Users\User\Desktop\clave_wp.txt"
SITE_URL = "https://huelvatv.com/wp-json/wp/v2"
USER = "Sergio"

MESES = {
    "01": "ENERO", "02": "FEBRERO", "03": "MARZO", "04": "ABRIL",
    "05": "MAYO", "06": "JUNIO", "07": "JULIO", "08": "AGOSTO",
    "09": "SEPTIEMBRE", "10": "OCTUBRE", "11": "NOVIEMBRE", "12": "DICIEMBRE"
}

def obtener_ids_etiquetas(etiquetas_texto, auth):
    """Busca en WP las etiquetas por nombre y devuelve sus IDs si existen."""
    if not etiquetas_texto:
        return []
        
    ids = []
    for nombre in etiquetas_texto:
        try:
            url_tag = f"{SITE_URL}/tags?search={nombre}"
            res = requests.get(url_tag, auth=auth)
            if res.status_code == 200:
                data = res.json()
                if data:
                    # Nos quedamos con la primera coincidencia
                    ids.append(data[0]['id'])
                    print(f" -> Etiqueta enlazada: {data[0]['name']} (ID: {data[0]['id']})")
        except Exception as e:
            print(f"Error buscando etiqueta '{nombre}': {e}")
    return ids

def generar_html_video(archivo_original):
    """Genera el bloque HTML del reproductor basándose en la fecha de hoy y el nombre original."""
    now = datetime.now()
    year = now.strftime("%Y")
    month_str = MESES[now.strftime("%m")]
    date_str = now.strftime("%d-%m-%y") # DD-MM-YY
    
    # Extraer el nombre original (sin extensión ni ruta)
    nombre_base = os.path.basename(archivo_original)
    nombre_sin_ext, _ = os.path.splitext(nombre_base)
    # Reconstruimos la extensión a mp4
    video_filename = f"{nombre_sin_ext}.mp4"
    
    # Usamos f-string para construir la URL. Los espacios en atributos web pueden dar problemas 
    # si no van codificados, pero en URLs completas es común usar urllib.parse o dejarlos si el servidor los traga.
    # WP y navegadores gestionan espacios si están dentro de los quotes del src="", pero para ser 100% seguros:
    from urllib.parse import quote
    
    # Encodeamos solo el nombre del archivo para que la URL sea válida internamente
    video_filename_safe = quote(video_filename)
    # El usuario pidió el formato estricto con espacios en el ejemplo. Los dejaremos tal cual el usuario pidió
    # src="https://videos.huelvatv.com/2026/NOTICIAS/FEBRERO/24-02-26/VTR BANDERAS DE ANDALUCÍA POR HUELVA.mp4"
    video_url = f"https://videos.huelvatv.com/{year}/NOTICIAS/{month_str}/{date_str}/{video_filename}"
    
    bloque = f'<figure class="wp-block-video"><video src="{video_url}" autoplay="autoplay" muted="" controls="controls" width="100%" height="auto"></video></figure>'
    return bloque


def publicar_articulo(archivo_json):
    if not os.path.exists(archivo_json):
        print(f"Error: No se encuentra el JSON {archivo_json}")
        sys.exit(1)
    if not os.path.exists(ARCHIVO_CLAVE):
        print(f"Error: Sin archivo de clave en {ARCHIVO_CLAVE}")
        sys.exit(1)

    with open(ARCHIVO_CLAVE, "r", encoding="utf-8") as f:
        APP_PASSWORD = f.read().strip().replace(" ", "")
    auth = HTTPBasicAuth(USER, APP_PASSWORD)

    with open(archivo_json, "r", encoding="utf-8") as f:
        datos = json.load(f)
        titulo = datos.get("titulo", "")
        entradilla = datos.get("entradilla", "")
        contenido_crudo = datos.get("contenido", "")
        etiquetas_sugeridas = datos.get("etiquetas", [])
        archivo_original = datos.get("archivo_original", "video_desconocido.mp4")

    if not titulo or not contenido_crudo:
        print("Error: El JSON no tiene formato válido.")
        sys.exit(1)

    print(f"Preparando artículo... Buscando etiquetas en WP...")
    tags_ids = obtener_ids_etiquetas(etiquetas_sugeridas, auth)

    print("Generando incrustación de vídeo HTML...")
    bloque_video = generar_html_video(archivo_original)
    
    # Separador estilo WordPress
    separador_html = '<hr class="wp-block-separator has-alpha-channel-opacity"/>'
    
    # Entradilla destacada
    bloque_entradilla = ""
    if entradilla:
        bloque_entradilla = f'<h3><em>{entradilla}</em></h3>'

    # Ensamblamos todo en orden: 
    # Video -> Separador -> Entradilla -> Cuerpo de la Noticia (que ya trae sus negritas)
    contenido_final = f"{bloque_video}\n\n{separador_html}\n\n{bloque_entradilla}\n\n{contenido_crudo}"

    post_data = {
        "title": titulo,
        "content": contenido_final,
        "excerpt": entradilla, # Usamos la entradilla como resumen en WP
        "status": "pending", 
        "tags": tags_ids
    }

    try:
        response = requests.post(f"{SITE_URL}/posts", auth=auth, json=post_data, allow_redirects=False)

        if response.status_code == 201:
            print("\n¡EXITO! Artículo creado como PENDIENTE de revisión.")
            print(f"URL de previsualización: {response.json().get('link')}")
            print("--------------------------------------------------")
            try:
                os.remove(archivo_json)
                print(f"Archivo temporal {archivo_json} eliminado.")
            except Exception: pass
        else:
            print(f"ERROR HTTP {response.status_code}")
            print(response.text)
            sys.exit(1)
    except Exception as e:
        print(f"EXCEPCIÓN CRÍTICA: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python publicar_wp.py <ruta_json>")
        sys.exit(1)
    publicar_articulo(sys.argv[1])
