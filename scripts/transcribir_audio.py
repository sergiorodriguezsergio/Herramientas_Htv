import sys
import os
import wave
import json
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer, SetLogLevel

# Configuración de rutas
FFMPEG_PATH = r"C:\Users\User\Documents\Antigravity\Projects\Herramientas_Htv\ffmpeg-master-latest-win64-gpl\bin"
os.environ["PATH"] += os.pathsep + FFMPEG_PATH

def transcribir(input_mp3, output_txt):
    SetLogLevel(-1) # Silenciar logs de Vosk
    
    # 1. Convertir MP3 a WAV (16kHz, mono, pcm_s16le)
    print(f"Convirtiendo {input_mp3} a formato compatible...")
    audio = AudioSegment.from_mp3(input_mp3)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    
    temp_wav = "temp_audio.wav"
    audio.export(temp_wav, format="wav")
    
    # 2. Cargar modelo y realizar transcripción
    # El modelo se descargará automáticamente si no existe en la carpeta 'model'
    model_path = "model"
    if not os.path.exists(model_path):
        print("Descargando modelo en español (esto puede tardar unos minutos la primera vez)...")
        import urllib.request
        import zipfile
        # Usamos el modelo pequeño para rapidez, o el grande para precisión. 
        # Forzamos descarga si no existe.
        model_url = "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip"
        urllib.request.urlretrieve(model_url, "model.zip")
        with zipfile.ZipFile("model.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        os.rename("vosk-model-small-es-0.42", model_path)
        os.remove("model.zip")

    model = Model(model_path)
    wf = wave.open(temp_wav, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    print("Transcribiendo...")
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part = json.loads(rec.Result())
            results.append(part.get("text", ""))
    
    final_res = json.loads(rec.FinalResult())
    results.append(final_res.get("text", ""))
    
    # 3. Guardar y limpiar
    transcripcion = " ".join(results).strip()
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(transcripcion)
    
    wf.close()
    os.remove(temp_wav)
    print(f"Transcripción completada. Guardada en: {output_txt}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python transcribir_audio.py <ruta_al_archivo_de_audio>")
        sys.exit(1)
        
    src = sys.argv[1]
    
    # Generar ruta de destino con el mismo nombre pero .txt
    nombre_base, _ = os.path.splitext(src)
    dst = f"{nombre_base}.txt"
    
    transcribir(src, dst)
