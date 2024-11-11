from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)


# Ruta para detectar el color en una imagen
@app.route('/colors', methods=['POST'])
def detect_color():
    # Lee la imagen enviada desde Flutter
    image = request.files['image'].read()
    # Convierte la imagen en un formato que OpenCV pueda leer
    np_img = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Procesa el color en el área central de la imagen
    color_name, hex_code, rgb_values = obtener_color_central(img)

    return jsonify({"color_name": color_name, "hex_code": hex_code, "rgb_values": rgb_values})


# Función para obtener el color promedio en el área central de la imagen
def obtener_color_central(img):
    height, width, _ = img.shape
    # Definir el área central (con un tamaño de 50x50 píxeles)
    center_area = img[height // 2 - 25:height // 2 + 25, width // 2 - 25:width // 2 + 25]

    # Calcular el color promedio de la zona central (BGR)
    avg_color = cv2.mean(center_area)[:3]  # Promedio de color (B, G, R)

    # Determinar el nombre del color
    color_name = determinar_nombre_color(avg_color)

    # Convertir el color promedio a formato hexadecimal
    hex_code = rgb_to_hex(avg_color)

    # Los valores RGB (BGR en OpenCV, por eso el orden es invertido)
    rgb_values = [int(avg_color[2]), int(avg_color[1]), int(avg_color[0])]  # [R, G, B]

    return color_name, hex_code, rgb_values


# Función para convertir el color RGB a hexadecimal
def rgb_to_hex(rgb):
    r, g, b = rgb
    return f'#{int(r):02x}{int(g):02x}{int(b):02x}'


def determinar_nombre_color(avg_color):
    r, g, b = avg_color[2], avg_color[1], avg_color[0]  # Extraemos los valores R, G, B de OpenCV (BGR)

    # Definición de colores básicos con rangos RGB
    if r > 150 and r < 255 and g > 0 and g < 70 and b > 0 and b < 70:
        return "Rojo"
    elif r < 255 and g > 0 and b < 120 and r > 160 and g < 65 and b > 105:
        return "Rosa"
    elif r < 255 and g > 0 and b < 255 and r > 130 and g < 75 and b > 130:
        return "Morado"
    elif r < 200 and g > 0 and b < 255 and r > 100 and g < 100 and b > 200:
        return "Morado"
    elif r < 170 and g > 0 and b < 255 and r > 70 and g < 70 and b > 100:
        return "Morado"
    elif r < 70 and r > 0 and g < 70 and g > 0 and b > 120 and b <255:
        return "Azul Oscuro"
    elif r > 0 and g > 100 and b > 150 and r < 75 and g < 255 and b < 255:
        return "Azul Claro"
    elif r > 0 and g > 155 and b > 155 and r < 100 and g < 255 and b < 255:
        return "Azul Cielo"
    elif r > 0 and g > 155 and b > 0 and r < 100 and g < 255 and b < 100:
        return "Verde"
    elif r > 100 and g > 155 and b > 0 and r < 200 and g < 255 and b < 100:
        return "Verde"
    elif r < 255 and g < 255 and b > 0 and r > 155 and g > 155 and b < 100:
        return "Amarillo"
    elif r < 255 and g < 200 and b > 0 and r > 180 and g > 160 and b < 70:
        return "Amarillo"
    elif r < 255 and g < 130 and b > 0 and r > 185 and g > 120 and b < 60:
        return "Naranja"
    elif r < 255 and g > 94 and b > 0 and r > 130 and g > 85 and  b < 65:
        return "Marrón"
    elif r < 255 and g > 0 and b > 0 and r > 155 and g < 80 and b < 80:
        return "Rojo"
    elif r < 100 and g < 100 and b < 100 and r > 0 and g > 0 and b > 0:
        return "Negro"
    elif r < 255 and g < 255 and b < 255 and r > 200 and b > 200 and b > 200:
        return "Blanco"
    elif r > 169 and g > 169 and b > 169 and r < 210 and g < 210 and b < 210:
        return "Gris"
    else:
        return "indefinido"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


