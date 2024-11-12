from flask import Flask, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)

model_path = "Modelos/best.pt"
model = YOLO(model_path)

label_map = {
    0: "Billete_20_Pesos_A",
    1: "Billete_20_Pesos_B",
    2: "Billete_20_Pesos_A_V",
    3: "Billete_20_Pesos_B_V",
    4: "Billete_50_Pesos_A",
    5: "Billete_50_Pesos_B",
    6: "Billete_50_Pesos_A_V",
    7: "Billete_50_Pesos_B_V"
}

@app.route("/predict", methods=["POST"])
def predict():
    # Verifica que haya un archivo de imagen
    if "image" not in request.files:
        return jsonify({"error": "No se encontró imagen"}), 400
    image_file = request.files["image"]

    # Lee y convierte la imagen
    np_image = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # Realiza la predicción usando el modelo
    results = model(image)
    predictions = []

    # Procesa los resultados
    for r in results[0].boxes:
        predictions.append({
            "label": label_map[int(r.cls)],  # Mapea la clase numérica a la etiqueta
            "confidence": float(r.conf) * 100,  # Convierte la confianza a porcentaje
            "box": {
                "x1": int(r.xyxy[0][0]),
                "y1": int(r.xyxy[0][1]),
                "x2": int(r.xyxy[0][2]),
                "y2": int(r.xyxy[0][3])
            }
        })

    return jsonify(predictions)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)