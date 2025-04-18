
import cv2
import mediapipe as mp
import numpy as np
import json

mp_pose = mp.solutions.pose

def distancia(p1, p2, ancho, alto):
    x1, y1 = int(p1.x * ancho), int(p1.y * alto)
    x2, y2 = int(p2.x * ancho), int(p2.y * alto)
    return np.linalg.norm([x2 - x1, y2 - y1])

def medir_cuerpo(ruta_imagen, ancho_cm_tarjeta=8.5, mostrar_vista_previa=True):
    image = cv2.imread(ruta_imagen)
    if image is None:
        return {"error": f"No se pudo cargar la imagen: {ruta_imagen}"}

    alto, ancho, _ = image.shape
    escala = 1.0

    # Detección de tarjeta de referencia (roja)
    tarjeta_mask = cv2.inRange(image, (0, 0, 100), (80, 80, 255))
    contours, _ = cv2.findContours(tarjeta_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        ancho_tarjeta_px = max(w, h)
        escala = ancho_cm_tarjeta / ancho_tarjeta_px

    with mp_pose.Pose(static_image_mode=True) as pose:
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.pose_landmarks:
            return {"error": "No se detectaron puntos del cuerpo"}

        puntos = results.pose_landmarks.landmark

        # FUNCIONES DE MEDIDA
        def px(p1, p2): return distancia(puntos[p1], puntos[p2], ancho, alto)

        medidas = {
            "espalda_cm": px(mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER) * escala,
            "busto_cm": px(mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER) * 1.1 * escala,
            "hombro_a_cintura_cm": distancia(puntos[mp_pose.PoseLandmark.LEFT_SHOULDER], puntos[mp_pose.PoseLandmark.LEFT_HIP], ancho, alto) * escala,
            "contorno_cintura_cm": px(mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP) * 2 * escala,
            "contorno_cadera_cm": px(mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP) * 2.2 * escala,
            "alto_busto_cm": distancia(puntos[mp_pose.PoseLandmark.LEFT_SHOULDER], puntos[mp_pose.PoseLandmark.LEFT_ELBOW], ancho, alto) * 0.5 * escala,
            "corte_imperio_cm": distancia(puntos[mp_pose.PoseLandmark.LEFT_SHOULDER], puntos[mp_pose.PoseLandmark.LEFT_ELBOW], ancho, alto) * 0.65 * escala,
            "largo_blusa_cm": distancia(puntos[mp_pose.PoseLandmark.LEFT_SHOULDER], puntos[mp_pose.PoseLandmark.LEFT_HIP], ancho, alto) * escala,
            "largo_vestido_cm": distancia(puntos[mp_pose.PoseLandmark.LEFT_SHOULDER], puntos[mp_pose.PoseLandmark.LEFT_ANKLE], ancho, alto) * escala,
            "largo_falda_cm": distancia(puntos[mp_pose.PoseLandmark.LEFT_HIP], puntos[mp_pose.PoseLandmark.LEFT_ANKLE], ancho, alto) * escala,
            "largo_manga_cm": px(mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_WRIST) * escala,
            "largo_pantalon_cm": px(mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_ANKLE) * escala,
            "escala_px_cm": escala
        }

        medidas_redondeadas = {k: round(v, 2) for k, v in medidas.items()}

        # Vista previa opcional
        if mostrar_vista_previa:
            annotated_image = image.copy()
            mp.solutions.drawing_utils.draw_landmarks(
                annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            for k, v in medidas_redondeadas.items():
                if "cm" in k:
                    print(f"{k}: {v} cm")
            cv2.imshow("Vista previa - Medidas del cuerpo", cv2.resize(annotated_image, (640, 480)))
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return medidas_redondeadas

# USO DE EJEMPLO:
if __name__ == "__main__":
    resultado = medir_cuerpo("foto_clienta.jpg", ancho_cm_tarjeta=8.5)
    print(json.dumps(resultado, indent=4))
