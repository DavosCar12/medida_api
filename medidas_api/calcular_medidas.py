import cv2
import mediapipe as mp
import numpy as np

def distancia_cm(p1, p2, img_w, referencia_pixeles_por_cm):
    dist = ((p2.x - p1.x)**2 + (p2.y - p1.y)**2) ** 0.5
    return (dist * img_w) / referencia_pixeles_por_cm

def calcular_todas_las_medidas(imagen_path, ancho_cm_tarjeta=8.5):
    mp_pose = mp.solutions.pose
    imagen = cv2.imread(imagen_path)
    alto, ancho, _ = imagen.shape

    # ---------------------------
    # DETECCIÓN DE POSE
    # ---------------------------
    with mp_pose.Pose(static_image_mode=True) as pose:
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        resultados = pose.process(imagen_rgb)

        if not resultados.pose_landmarks:
            return {"error": "No se detectaron puntos clave en la imagen"}

        lm = resultados.pose_landmarks.landmark

    # ---------------------------
    # CÁLCULO DE REFERENCIA CON TARJETA
    # ---------------------------
    tarjeta_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    _, tarjeta_bin = cv2.threshold(tarjeta_gris, 245, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(tarjeta_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    tarjeta_mayor = max(contornos, key=cv2.contourArea) if contornos else None

    if tarjeta_mayor is None:
        return {"error": "No se detectó la tarjeta blanca de referencia"}

    x, y, w, h = cv2.boundingRect(tarjeta_mayor)
    pixeles_por_cm = w / ancho_cm_tarjeta

    # ---------------------------
    # CÁLCULO DE MEDIDAS
    # ---------------------------
    medidas = {
        "ancho_hombros_cm": distancia_cm(lm[11], lm[12], ancho, pixeles_por_cm),
        "ancho_espalda_cm": distancia_cm(lm[11], lm[12], ancho, pixeles_por_cm),
        "ancho_cintura_cm": distancia_cm(lm[23], lm[24], ancho, pixeles_por_cm),
        "ancho_cadera_cm": distancia_cm(lm[25], lm[26], ancho, pixeles_por_cm),
        "alto_busto_cm": distancia_cm(lm[11], lm[23], ancho, pixeles_por_cm),
        "corte_imperio_cm": distancia_cm(lm[11], lm[24], ancho, pixeles_por_cm),
        "largo_blusa_cm": distancia_cm(lm[11], lm[27], ancho, pixeles_por_cm),
        "largo_vestido_cm": distancia_cm(lm[11], lm[31], ancho, pixeles_por_cm),
        "largo_falda_cm": distancia_cm(lm[23], lm[31], ancho, pixeles_por_cm),
        "largo_manga_izq_cm": distancia_cm(lm[11], lm[15], ancho, pixeles_por_cm),
        "largo_manga_der_cm": distancia_cm(lm[12], lm[16], ancho, pixeles_por_cm),
        "hombro_a_cintura_cm": distancia_cm(lm[11], lm[23], ancho, pixeles_por_cm),
    }

    medidas_redondeadas = {k: round(v, 2) for k, v in medidas.items()}

    return {
        "medidas_cm": medidas_redondeadas,
        "mensaje": "✅ Medidas calculadas correctamente"
    }

