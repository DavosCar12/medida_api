from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from calcular_medidas import calcular_todas_las_medidas  # Asegúrate de que este archivo existe

app = FastAPI()

# Habilita CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes ajustar esto por seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/medir")
async def medir(imagen: UploadFile = File(...), ancho_cm_tarjeta: float = 8.5):
    try:
        # Guardamos el archivo subido
        contenido = await imagen.read()
        nombre_archivo = f"imagenes/{imagen.filename}"
        with open(nombre_archivo, "wb") as f:
            f.write(contenido)

        # Llamamos a la función para calcular medidas
        resultado = calcular_todas_las_medidas(nombre_archivo, ancho_cm_tarjeta=ancho_cm_tarjeta)
        return resultado

    except Exception as e:
        return {"error": str(e)}


        medidas = calcular_todas_las_medidas(image, ancho_cm_tarjeta=8.5)
        return medidas
    except Exception as e:
        return {"error": str(e)}


@app.get("/")
def inicio():
    return {"mensaje": "API de medición corporal funcionando"}

