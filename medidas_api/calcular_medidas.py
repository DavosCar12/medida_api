import cv2
import mediapipe as mp

def calcular_todas_las_medidas(imagen_path, altura_persona_cm=190.0):
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(static_image_mode=True) as pose:
        imagen = cv2.imread(imagen_path)
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        resultados = pose.process(imagen_rgb)

        if not resultados.pose_landmarks:
            return {"error": "No se detectaron puntos clave en la imagen"}

        landmarks = resultados.pose_landmarks.landmark
        alto_imagen = imagen.shape[0]
        ancho_imagen = imagen.shape[1]

        def pixel(p):
            return int(p.x * ancho_imagen), int(p.y * alto_imagen)

        # Altura total (de cabeza a tobillos)
        cabeza = landmarks[0]
        tobillo_izq = landmarks[27]
        tobillo_der = landmarks[28]

        y_cabeza = cabeza.y * alto_imagen
        y_tobillo = min(tobillo_izq.y, tobillo_der.y) * alto_imagen

        altura_pixeles = abs(y_tobillo - y_cabeza)
        if altura_pixeles == 0:
            return {"error": "La altura en píxeles es cero. Verifica la imagen."}

        pixeles_por_cm = altura_pixeles / altura_persona_cm

        def medir(p1, p2):
            x1, y1 = pixel(p1)
            x2, y2 = pixel(p2)
            dist_pixeles = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
            return round(dist_pixeles / pixeles_por_cm, 2)

        hombro_izq = landmarks[11]
        hombro_der = landmarks[12]
        cadera_izq = landmarks[23]
        cadera_der = landmarks[24]
        cintura_izq = landmarks[23]  # Se aproxima en esta versión
        cintura_der = landmarks[24]
        codo_izq = landmarks[13]
        codo_der = landmarks[14]
        muñeca_izq = landmarks[15]
        muñeca_der = landmarks[16]

        largo_blusa = medir(hombro_der, cadera_der)
        largo_vestido = medir(hombro_der, tobillo_der)
        largo_falda = medir(cadera_der, tobillo_der)
        alto_busto = medir(hombro_der, landmarks[11])  # aproximado
        corte_imperio = medir(hombro_der, landmarks[23])  # hombro a cadera como proxy

        medidas = {
            "ancho_hombros_cm": medir(hombro_izq, hombro_der),
            "ancho_espalda_cm": medir(hombro_izq, hombro_der),  # Igual que hombros por ahora
            "ancho_cintura_cm": medir(cintura_izq, cintura_der),
            "ancho_cadera_cm": medir(cadera_izq, cadera_der),
            "alto_busto_cm": alto_busto,
            "corte_imperio_cm": corte_imperio,
            "largo_blusa_cm": largo_blusa,
            "largo_vestido_cm": largo_vestido,
            "largo_falda_cm": largo_falda,
            "largo_manga_izq_cm": medir(hombro_izq, muñeca_izq),
            "largo_manga_der_cm": medir(hombro_der, muñeca_der),
            "hombro_a_cintura_cm": medir(hombro_der, landmarks[23]),
        }

        return {
            "medidas_cm": medidas,
            "mensaje": "✅ Medidas calculadas correctamente con base en la altura."
        }

