# calcular_medidas.py

import cv2
import mediapipe as mp

def calcular_todas_las_medidas(imagen_path, ancho_cm_tarjeta=None):
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(static_image_mode=True) as pose:
        imagen = cv2.imread(imagen_path)
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        resultados = pose.process(imagen_rgb)

        if not resultados.pose_landmarks:
            return {"error": "No se detectaron puntos clave en la imagen"}

        landmarks = resultados.pose_landmarks.landmark

        hombro_izq = landmarks[11]
        hombro_der = landmarks[12]

        dist_hombros = ((hombro_der.x - hombro_izq.x) ** 2 + (hombro_der.y - hombro_izq.y) ** 2) ** 0.5

        # Determinar el factor de conversión
        if ancho_cm_tarjeta:
            ancho_pixeles_tarjeta = imagen.shape[1]  # Suponiendo que la tarjeta ocupa todo el ancho
            pixeles_por_cm = ancho_pixeles_tarjeta / ancho_cm_tarjeta
        else:
            pixeles_por_cm = 30  # valor por defecto

        hombros_cm = dist_hombros * imagen.shape[1] / pixeles_por_cm

        return {
            "distancia_hombros_cm": round(hombros_cm, 2),
            "mensaje": "Medidas calculadas correctamente."
        }
