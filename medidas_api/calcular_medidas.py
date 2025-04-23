# calcular_medidas.py

import cv2
import mediapipe as mp

def calcular_todas_las_medidas(imagen_path, ancho_cm_tarjeta=None):
    mp_pose = mp.solutions.pose

    def distancia(p1, p2):
        return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5 * imagen.shape[1] / pixeles_por_cm

    with mp_pose.Pose(static_image_mode=True) as pose:
        imagen = cv2.imread(imagen_path)
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        resultados = pose.process(imagen_rgb)

        if not resultados.pose_landmarks:
            return {"error": "No se detectaron puntos clave en la imagen"}

        landmarks = resultados.pose_landmarks.landmark

        # Factor de conversión
        if ancho_cm_tarjeta:
            ancho_pixeles_tarjeta = imagen.shape[1]
            pixeles_por_cm = ancho_pixeles_tarjeta / ancho_cm_tarjeta
        else:
            pixeles_por_cm = 30  # Valor por defecto

        # Extraer puntos
        p = landmarks  # alias para acortar

        # Calcular medidas
        medidas = {
            "ancho_hombros_cm": round(distancia(p[11], p[12]), 2),
            "ancho_espalda_cm": round(distancia(p[11], p[12]), 2),  # similar a hombros
            "ancho_cintura_cm": round(distancia(p[23], p[24]), 2),
            "ancho_cadera_cm": round(distancia(p[25], p[26]), 2),
            "alto_busto_cm": round(distancia(p[11], p[13]), 2),
            "corte_imperio_cm": round(distancia(p[11], p[23]) * 0.6, 2),
            "largo_blusa_cm": round(distancia(p[11], p[23]), 2),
            "largo_vestido_cm": round(distancia(p[11], p[27]), 2),
            "largo_falda_cm": round(distancia(p[23], p[27]), 2),
            "largo_manga_izq_cm": round(distancia(p[11], p[15]), 2),
            "largo_manga_der_cm": round(distancia(p[12], p[16]), 2),
            "hombro_a_cintura_cm": round(distancia(p[11], p[23]), 2)
        }

        return {
            "medidas_cm": medidas,
            "mensaje": "✅ Medidas calculadas correctamente"
        }
