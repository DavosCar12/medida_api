import cv2
import mediapipe as mp
import math

def distancia_entre(p1, p2, imagen_shape=None, altura_persona_cm=None):
    # Distancia en pixeles
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distancia = math.sqrt(dx ** 2 + dy ** 2)

    if imagen_shape and altura_persona_cm:
        altura_px = imagen_shape[0]  # altura de la imagen en pixeles
        pixeles_por_cm = altura_px / altura_persona_cm
        return distancia * imagen_shape[0] / pixeles_por_cm

    return distancia

def calcular_todas_las_medidas(imagen_path, altura_cm=160, peso_kg=60):
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(static_image_mode=True) as pose:
        imagen = cv2.imread(imagen_path)
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        resultados = pose.process(imagen_rgb)

        if not resultados.pose_landmarks:
            return {"error": "No se detectaron puntos clave en la imagen"}

        landmarks = resultados.pose_landmarks.landmark

        # Puntos clave
        hombro_izq = landmarks[11]
        hombro_der = landmarks[12]
        cadera_izq = landmarks[23]
        cadera_der = landmarks[24]
        codo_izq = landmarks[13]
        muneca_izq = landmarks[15]
        codo_der = landmarks[14]
        muneca_der = landmarks[16]
        cintura_y = (landmarks[23].y + landmarks[24].y) / 2
        busto_y = (landmarks[11].y + landmarks[12].y) / 2
        rodilla_izq = landmarks[25]
        tobillo_izq = landmarks[27]

        alto_busto_cm = distancia_entre(hombro_izq, cadera_izq, imagen.shape, altura_cm)
        corte_imperio_cm = distancia_entre(hombro_izq, landmarks[24], imagen.shape, altura_cm)
        largo_blusa_cm = distancia_entre(hombro_izq, landmarks[24], imagen.shape, altura_cm)  # hasta la cadera
        largo_vestido_cm = distancia_entre(hombro_izq, tobillo_izq, imagen.shape, altura_cm)
        largo_falda_cm = distancia_entre(cadera_izq, tobillo_izq, imagen.shape, altura_cm)
        largo_manga_izq_cm = distancia_entre(hombro_izq, muneca_izq, imagen.shape, altura_cm)
        largo_manga_der_cm = distancia_entre(hombro_der, muneca_der, imagen.shape, altura_cm)
        hombro_a_cintura_cm = distancia_entre(hombro_izq, landmarks[23], imagen.shape, altura_cm)

        # Cálculos de anchos
        ancho_espalda_cm = distancia_entre(hombro_izq, hombro_der, imagen.shape, altura_cm)
        ancho_hombros_cm = ancho_espalda_cm

        # Estimaciones con peso para medidas de contorno (opcional)
        ancho_cintura_cm = peso_kg * 0.9  # puedes mejorar esta fórmula
        ancho_cadera_cm = peso_kg * 1.1

        return {
            "medidas_cm": {
                "ancho_hombros_cm": round(ancho_hombros_cm, 2),
                "ancho_espalda_cm": round(ancho_espalda_cm, 2),
                "ancho_cintura_cm": round(ancho_cintura_cm, 2),
                "ancho_cadera_cm": round(ancho_cadera_cm, 2),
                "alto_busto_cm": round(alto_busto_cm, 2),
                "corte_imperio_cm": round(corte_imperio_cm, 2),
                "largo_blusa_cm": round(largo_blusa_cm, 2),
                "largo_vestido_cm": round(largo_vestido_cm, 2),
                "largo_falda_cm": round(largo_falda_cm, 2),
                "largo_manga_izq_cm": round(largo_manga_izq_cm, 2),
                "largo_manga_der_cm": round(largo_manga_der_cm, 2),
                "hombro_a_cintura_cm": round(hombro_a_cintura_cm, 2)
            },
            "mensaje": "✅ Medidas calculadas correctamente con base en la altura."
        }

