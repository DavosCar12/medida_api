# calcular_medidas.py

import cv2
import mediapipe as mp


def calcular_todas_las_medidas(imagen_path, altura_cm=160, peso_kg=60):
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(static_image_mode=True) as pose:
        imagen = cv2.imread(imagen_path)
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        resultados = pose.process(imagen_rgb)

        if not resultados.pose_landmarks:
            return {"error": "No se detectaron puntos clave en la imagen"}

        landmarks = resultados.pose_landmarks.landmark
        height, width, _ = imagen.shape

        def distancia(p1, p2):
            return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2) ** 0.5 * height

        hombro_izq = landmarks[11]
        hombro_der = landmarks[12]
        cadera_izq = landmarks[23]
        cadera_der = landmarks[24]
        cintura_izq = landmarks[11]
        cintura_der = landmarks[12]
        codo_izq = landmarks[13]
        muneca_izq = landmarks[15]
        codo_der = landmarks[14]
        muneca_der = landmarks[16]
        cadera = ((cadera_der.x + cadera_izq.x) / 2, (cadera_der.y + cadera_izq.y) / 2)
        hombro = ((hombro_der.x + hombro_izq.x) / 2, (hombro_der.y + hombro_izq.y) / 2)

        # Escalado en cm
        altura_px = abs(landmarks[0].y - landmarks[32].y) * height
        px_por_cm = altura_px / altura_cm

        # Ajuste proporcional con peso
        factor_peso = peso_kg / 60  # 60kg como referencia

        medidas = {
            "ancho_hombros_cm": round(distancia(hombro_izq, hombro_der) / px_por_cm * factor_peso, 2),
            "ancho_espalda_cm": round(distancia(hombro_izq, hombro_der) / px_por_cm * factor_peso, 2),
            "ancho_cintura_cm": round(distancia(cintura_izq, cintura_der) / px_por_cm * factor_peso, 2),
            "ancho_cadera_cm": round(distancia(cadera_izq, cadera_der) / px_por_cm * factor_peso, 2),
            "alto_busto_cm": round(abs(hombro_izq.y - cadera_izq.y) * height / px_por_cm, 2),
            "corte_imperio_cm": round(abs(hombro_izq.y - cadera_izq.y) * height / px_por_cm * 1.1, 2),
            "largo_blusa_cm": round(abs(hombro_izq.y - cadera_izq.y) * height / px_por_cm * 1.3, 2),
            "largo_vestido_cm": round(abs(landmarks[11].y - landmarks[27].y) * height / px_por_cm, 2),
            "largo_falda_cm": round(abs(landmarks[23].y - landmarks[27].y) * height / px_por_cm, 2),
            "largo_manga_izq_cm": round(distancia(hombro_izq, codo_izq) + distancia(codo_izq, muneca_izq) / px_por_cm, 2),
            "largo_manga_der_cm": round(distancia(hombro_der, codo_der) + distancia(codo_der, muneca_der) / px_por_cm, 2),
            "hombro_a_cintura_cm": round(abs(hombro_izq.y - cadera_izq.y) * height / px_por_cm, 2),
        }

        return {
            "medidas_cm": medidas,
            "mensaje": "✅ Medidas calculadas correctamente con base en altura y peso."
        }


