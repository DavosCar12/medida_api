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
async def medir(imagen: UploadFile = File(...)):
    contents = await imagen.read()
    image_np = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    medidas = calcular_todas_las_medidas(image, ancho_cm_tarjeta=8.5)
    return medidas

@app.get("/")
def inicio():
    return {"mensaje": "API de medición corporal funcionando"}

