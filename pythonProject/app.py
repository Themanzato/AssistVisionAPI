from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)


# Ruta para detectar el color en una imagen
@app.route('/detect_color', methods=['POST'])
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
    r, g, b = avg_color[2], avg_color[1], avg_color[0]

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
    elif r > 160 and g > 120 and b > 170 and r < 170 and g < 140 and b < 190:
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
    elif r < 50 and g < 50 and b < 50 and r > 0 and g > 0 and b > 0:
        return "Negro"
    elif r < 255 and g < 255 and b < 255 and r > 200 and b > 200 and b > 200:
        return "Blanco"
    elif r > 169 and g > 169 and b > 169 and r < 210 and g < 210 and b < 210:
        return "Gris"
    elif r > 70 and g > 70 and b > 70 and r < 100 and g < 100 and b < 100:
        return "Gris"
    elif r > 100 and g > 100 and b > 100 and r < 120 and g < 120 and b < 120:
        return "Gris"
    elif r > 120 and g > 120 and b > 120 and r < 140 and g < 140 and b < 140:
        return "Gris"
    elif r > 140 and g > 140 and b > 140 and r < 160 and g < 169 and b < 169:
        return "Gris"
    #VARIACIONES DE COLORES INDEFINIDOS
    elif r >= 200 and r <= 255 and g >= 70 and g <= 120 and b >= 50 and b <= 90:
        return "Rojo Claro"
    elif r >= 180 and r <= 210 and g >= 160 and g <= 200 and b >= 100 and b <= 140:
        return "Dorado"
    elif r >= 140 and r <= 170 and g >= 110 and g <= 140 and b >= 60 and b <= 90:
        return "Café"
    elif r > 120 and g > 100 and b < 50 and r < 130 and g < 120 and b < 60:
        return "Café"
    elif r >= 150 and r <= 170 and g >= 150 and g <= 170 and b >= 140 and b <= 160:
        return "Gris"
    elif r >= 150 and r <= 170 and g >= 160 and g <= 180 and b >= 120 and b <= 140:
        return "Gris"
    elif r >= 145 and r <= 155 and g >= 145 and g <= 155 and b >= 120 and b <= 135:
        return "Gris"
    elif r >= 130 and r <= 150 and g >= 140 and g <= 160 and b >= 75 and b <= 90:
        return "Verde Lima"
    elif r >= 150 and r <= 160 and g >= 150 and g <= 165 and b >= 110 and b <= 120:
        return "Gris"
    elif r >= 160 and r <= 180 and g >= 180 and g <= 200 and b >= 120 and b <= 140:
        return "Verde Lima"
    elif r >= 140 and r <= 150 and g >= 130 and g <= 150 and b >= 110 and b <= 120:
        return "Gris"
    elif r >= 110 and r <= 130 and g >= 100 and g <= 120 and b >= 70 and b <= 90:
        return "Marrón"
    elif r >= 100 and r <= 120 and g >= 90 and g <= 110 and b >= 60 and b <= 80:
        return "Marrón"
    elif r >= 140 and r <= 150 and g >= 130 and g <= 140 and b >= 120 and b <= 130:
        return "Gris"
    elif r >= 150 and r <= 170 and g >= 180 and g <= 200 and b >= 100 and b <= 120:
        return "Verde Claro"
    elif r >= 120 and r <= 130 and g >= 120 and g <= 130 and b >= 90 and b <= 110:
        return "Gris"
    elif r >= 120 and r <= 135 and g >= 115 and g <= 130 and b >= 110 and b <= 125:
        return "Gris"
    elif r >= 125 and r <= 135 and g >= 115 and g <= 125 and b >= 100 and b <= 115:
        return "Gris"
    elif r > 130 and g > 130 and b > 130 and r < 160 and g < 160 and b < 160:
        return "Gris"
    elif r > 100 and g > 100 and b > 130 and r < 120 and g < 120 and b < 150:
        return "Gris"
    elif r > 60 and g > 60 and b > 60 and r < 80 and g < 80 and b < 80:
        return "Gris"
    elif r > 130 and g > 120 and b > 160 and r < 140 and g < 130 and b < 170:
        return "Gris"
    elif r >= 65 and r <= 80 and g >= 10 and g <= 25 and b >= 10 and b <= 25:
        return "Vino"
    elif r >= 90 and r <= 100 and g >= 15 and g <= 30 and b >= 10 and b <= 30:
        return "Vino"
    elif r >= 40 and r <= 60 and g >= 5 and g <= 20 and b >= 5 and b <= 20:
        return "Vino"
    elif r > 10 and r < 40 and g > 70 and g < 90 and b > 160 and b < 190:
        return "Azul"

    elif r > 30 and g > 30 and b > 50 and r < 70 and g < 50 and b < 100:
        return "Azul Marino"
    elif r > 60 and g > 60 and b > 120 and r < 100 and g < 100 and b < 150:
        return "Azul Marino"
    elif r > 0 and g > 10 and b > 50 and r < 20 and g < 30 and b < 70:
        return "Azul Marino"
    elif r > 50 and g > 60 and b > 100 and r < 60 and g < 70 and b < 110:
        return "Azul Marino"
    elif r > 40 and g > 60 and b > 100 and r < 50 and g < 70 and b < 110:
        return "Azul Marino"
    elif r > 50 and g < 30 and b > 20 and r < 70 and g < 30 and b < 50:
        return "Vino"
    elif r > 60 and g < 50 and b > 60 and r < 80 and g < 50 and b < 80:
        return "Morado"
    elif r > 160 and g > 130 and b > 150 and r < 180 and g < 150 and b < 170:
        return "Morado"
    elif r > 240 and g > 170 and b < 120 and r < 255 and g < 200 and b < 120:
        return "Naranja"
    elif r > 190 and g > 100 and b > 120 and r < 210 and g < 130 and b < 150:
        return "Rosa"
    elif r > 180 and g > 110 and b > 130 and r < 190 and g < 130 and b < 160:
        return "Rosa"
    elif r > 150 and g > 210 and b > 130 and r < 160 and g < 230 and b < 140:
        return "Amarillo Claro"

    else:
        return "indefinido"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)


