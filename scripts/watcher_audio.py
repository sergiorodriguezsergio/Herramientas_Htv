import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuración
CARPETA_VIGILADA = r"C:\Users\Equipo1\Desktop\AUDIO"
EXTENSIONES_PERMITIDAS = (".mp3", ".wav")
# La ruta al script o comando que lance el workflow de Antigravity
# De momento lo imprimiremos hasta que definamos el comando exacto para el workflow
COMANDO_WORKFLOW = "antigravity run procesar_audio" 

class ManejadorNuevosAudios(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            archivo = event.src_path
            nombre, extension = os.path.splitext(archivo)
            
            if extension.lower() in EXTENSIONES_PERMITIDAS:
                print(f"[{time.strftime('%H:%M:%S')}] ¡Nuevo audio detectado!: {os.path.basename(archivo)}")
                # Esperamos un momento para asegurarnos de que el archivo terminó de copiarse
                time.sleep(2)
                self.procesar_audio(archivo)

    def procesar_audio(self, ruta_archivo):
        print(f"[{time.strftime('%H:%M:%S')}] Iniciando Workflow de Antigravity para: {ruta_archivo}")
        
        # Aquí lanzaremos el comando para que Antigravity actúe.
        # Por ahora lo mostramos por pantalla simulando la llamada.
        # En el paso de integración real con la CLI de Antigravity lo ajustaremos.
        print(f"Ejecutando orquestador sobre: {ruta_archivo}")
        # subprocess.run([COMANDO_WORKFLOW, ruta_archivo])
        print("-------------")

if __name__ == "__main__":
    # Si la carpeta no existe, la creamos (aunque sabemos que en este equipo sí existe)
    if not os.path.exists(CARPETA_VIGILADA):
        os.makedirs(CARPETA_VIGILADA)

    event_handler = ManejadorNuevosAudios()
    observer = Observer()
    observer.schedule(event_handler, CARPETA_VIGILADA, recursive=False)
    observer.start()
    
    print(f"Ojos muy abiertos. Vigilando la carpeta: {CARPETA_VIGILADA}")
    print("Buscando nuevos archivos .mp3 o .wav... Presiona CTRL+C para detener.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nVigilancia terminada.")
        
    observer.join()
