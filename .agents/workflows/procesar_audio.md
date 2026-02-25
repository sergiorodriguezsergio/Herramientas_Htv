---
description: Procesa un archivo de audio (.mp3 o .wav), transcribe su contenido, redacta una noticia periodística (estilo Huelva TV) y la publica en WordPress.
// turbo-all
---

Este workflow se encarga de todo el flujo automatizado: desde un archivo de audio crudo hasta el artículo final publicado en la web.

Asegúrate de recibir la ruta completa del audio como parámetro. Por ejemplo, al iniciar el workflow el usuario te dirá algo como: "Aplica este workflow sobre este archivo C:\ruta\test.mp3".

1. **Obtener la ruta del audio:** Confirma la ruta absoluta del archivo de audio que el usuario te ha pasado o que el watcher ha detectado.

2. **Ejecutar transcripción local:**
   - Ejecuta el siguiente script en la terminal (asegúrate de usar la ruta base del proyecto `C:\Users\Equipo1\Documents\Antigravity\Projects\Herramientas_Htv`):
   `py scripts\transcribir_audio.py "RUTA_DEL_AUDIO"`
   - Sustituye `"RUTA_DEL_AUDIO"` por la ruta analizada en el paso 1.
   - Usa `command_status` para esperar a que termine (puede tardar un poco dependiendo del audio, ya que utiliza el modelo Vosk local).

3. **Leer la transcripción:**
   - Averigua el nombre del archivo de texto generado (mismo nombre que el audio pero con extensión `.txt`).
   - Usa la herramienta `view_file` para leer el contenido de esa transcripción cruda.

4. **Redactar el artículo periodístico:**
   - Toma esa transcripción cruda y redacta internamente una noticia para `www.huelvatv.com`.
   - **Reglas estrictas de redacción:**
      - Estilo formal, objetivo y periodístico.
      - Extensión entre 200 y 250 palabras, estructurado en máximo 3 párrafos.
      - **Entradilla**: Redacta una entradilla (resumen breve y atractivo de 2-3 líneas).
      - **Negritas**: Aplica formato HTML usando la etiqueta `<strong>` para resaltar nombres importantes, datos clave o frases relevantes dentro del texto.
      - NO incluyas valoraciones subjetivas del periodista ni conclusiones al final.
      - Titular descriptivo e informativo (de unas 15 palabras).
      - Piensa en varias etiquetas oportunas para categorizarlo (ej. nombres propios, temáticas, ubicaciones relevantes).

5. **Verificación Humana (Llamada a Skill Externa):**
   - Una vez redactada la noticia, guárdala en un archivo temporal llamado `noticia_generada.json` en la raíz del proyecto. El JSON debe tener esta estructura exacta:
   `{"titulo": "Titular de ejemplo", "entradilla": "Resumen breve...", "contenido": "<p>Párrafo 1 en <strong>negrita</strong>...</p>", "archivo_original": "nombre_exacto_del_audio.mp3", "etiquetas": ["Etiqueta1", "Etiqueta 2"]}`
   - **DETÉN EL FLUJO AQUÍ Y LLAMA A LA SKILL: `Verificador_Textos`.**
   - Muéstrale al usuario el Título, Entradilla, Contenido y Etiquetas generadas y pídele que los revise.
   - Aplica las reglas del verificador (busca nombres propios en la web para contrastarlos y dale las fuentes al usuario).
   - **SOLO cuando el usuario te dé el "OK" explícito**, podrás continuar al paso 6. Si pide cambios, modifica el JSON y vuelve a pedir el OK.

// turbo
6. **Publicar en WordPress:**
   - Tras el OK del usuario, ejecuta el siguiente comando:
   `py scripts\publicar_wp.py "noticia_generada.json"`
   - Esto subirá el contenido verificado a la web de Huelva TV.

7. **Limpieza y Cierre:**
   - Borra el archivo de audio original y el archivo de texto de la transcripción para dejar la carpeta limpia y lista para el próximo archivo.
   - Notifica al usuario que el proceso ha terminado con éxito y proporciónale la URL o el estado devuelto por el script de publicación.
