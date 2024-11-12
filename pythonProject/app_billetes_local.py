from flask import Flask, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)

# Ruta del modelo
model_path = "./Modelo/best.pt"
model = YOLO(model_path)

# Diccionario de mapeo de etiquetas a billetes
label_map = {
    0: "Billete de 20 pesos",
    1: "Billete de 20 pesos",
    2: "Billete de 20 pesos",
    3: "Billete de 20 pesos",
    4: "Billete de 50 pesos",
    5: "Billete de 50 pesos",
    6: "Billete de 50 pesos",
    7: "Billete de 50 pesos"
}

# Umbral de confianza
confidence_threshold = 85  # Ajusta este valor según tus necesidades

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No se encontró imagen"}), 400

    # Lee la imagen
    image_file = request.files["image"]
    np_image = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # Realiza la predicción usando el modelo
    results = model(image)
    predictions = []

    # Procesa los resultados de detección, aplicando el umbral de confianza
    for r in results[0].boxes:
        confidence = float(r.conf) * 100  # Convierte la confianza a porcentaje
        if confidence >= confidence_threshold:  # Solo añade predicciones por encima del umbral
            label_id = int(r.cls)
            label = label_map.get(label_id, "Etiqueta desconocida")
            predictions.append({
                "label": label,
                "confidence": round(confidence, 2),  # Redondea el porcentaje a 2 decimales
                "box": {
                    "x1": int(r.xyxy[0][0]),
                    "y1": int(r.xyxy[0][1]),
                    "x2": int(r.xyxy[0][2]),
                    "y2": int(r.xyxy[0][3])
                }
            })

    # Verifica si no se detectaron billetes con suficiente confianza
    if not predictions:
        return jsonify({"message": "No se detectó ningún billete con suficiente confianza en la imagen"}), 200

    return jsonify(predictions)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
