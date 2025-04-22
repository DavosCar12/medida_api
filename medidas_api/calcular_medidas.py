# calcular_medidas.py

import cv2
import mediapipe as mp

def calcular_todas_las_medidas(imagen_path):
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(static_image_mode=True) as pose:
        imagen = cv2.imread(imagen_path)
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        resultados = pose.process(imagen_rgb)

        if not resultados.pose_landmarks:
            return {"error": "No se detectaron puntos clave en la imagen"}

        landmarks = resultados.pose_landmarks.landmark

        # Ejemplo de cómo medir la distancia entre los hombros (landmarks 11 y 12)
        hombro_izq = landmarks[11]
        hombro_der = landmarks[12]

        # Calculamos la distancia euclidiana en píxeles
        dist_hombros = ((hombro_der.x - hombro_izq.x) ** 2 + (hombro_der.y - hombro_izq.y) ** 2) ** 0.5

        # Opcional: conversión a cm usando una referencia si la tienes
        # Suponiendo que tienes un factor de conversión "pixeles_por_cm"
        pixeles_por_cm = 30  # Esto es solo un ejemplo, se debe calcular con referencia visual
        hombros_cm = dist_hombros * imagen.shape[1] / pixeles_por_cm

        return {
            "distancia_hombros_cm": round(hombros_cm, 2),
            "mensaje": "Medidas calculadas correctamente."
        }
