from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import mediapipe as mp
from calcular_medidas import calcular_todas_las_medidas  # Este archivo lo debes tener tú

app = Flask(__name__)
CORS(app)

@app.route('/medir', methods=['POST'])
def medir():
    if 'imagen' not in request.files:
        return jsonify({'error': 'No se encontró ninguna imagen'}), 400

    file = request.files['imagen']
    image_np = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    medidas = calcular_todas_las_medidas(image, ancho_cm_tarjeta=8.5)
    return jsonify(medidas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

