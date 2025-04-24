from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
from calcular_medidas import calcular_todas_las_medidas

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
async def medir(
    imagen: UploadFile = File(...),
    altura_cm: float = Form(...),
    peso_kg: float = Form(...)
):
    try:
        # Crear carpeta si no existe
        os.makedirs("imagenes", exist_ok=True)

        # Guardar la imagen
        contenido = await imagen.read()
        nombre_archivo = f"imagenes/{imagen.filename}"
        with open(nombre_archivo, "wb") as f:
            f.write(contenido)

        # Llamar la función de medición
        resultado = calcular_todas_las_medidas(nombre_archivo, altura_cm=altura_cm, peso_kg=peso_kg)
        return resultado

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def inicio():
    return {"mensaje": "API de medición corporal funcionando"}

