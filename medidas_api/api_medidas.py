
from flask import Flask, request, jsonify
from medir_cuerpo_completo import medir_cuerpo
import os

app = Flask(__name__)

@app.route("/medir", methods=["POST"])
def medir():
    if "imagen" not in request.files:
        return jsonify({"error": "No se encontró ninguna imagen"}), 400

    archivo = request.files["imagen"]
    ruta_temporal = "foto_clienta.jpg"
    archivo.save(ruta_temporal)

    try:
        resultado = medir_cuerpo(ruta_temporal, ancho_cm_tarjeta=8.5, mostrar_vista_previa=False)
        os.remove(ruta_temporal)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
