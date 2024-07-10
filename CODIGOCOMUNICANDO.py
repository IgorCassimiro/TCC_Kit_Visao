import cv2
import numpy as np
import urllib.request
import serial
import time

# Configurar a comunicação serial
ser = serial.Serial('COM5', 9600)  # Altere 'COM3' para a porta serial correta

# Função para aumentar a saturação das cores na imagem
def aumentar_saturacao(imagem, alpha=3, beta=0):
    # Converter a imagem para o espaço de cores HSV
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
    
    # Separar os canais de cor
    h, s, v = cv2.split(hsv)
    
    # Aumentar a saturação
    saturacao_aumentada = cv2.multiply(s, alpha)
    
    # Normalizar a saturação aumentada para o intervalo [0, 255]
    saturacao_aumentada = cv2.normalize(saturacao_aumentada, None, 0, 255, cv2.NORM_MINMAX)
    saturacao_aumentada = np.uint8(saturacao_aumentada)
    
    # Juntar os canais de cor novamente
    hsv_saturacao_aumentada = cv2.merge([h, saturacao_aumentada, v])
    
    # Converter de volta para o espaço de cores BGR
    imagem_saturacao_aumentada = cv2.cvtColor(hsv_saturacao_aumentada, cv2.COLOR_HSV2BGR)
    
    return imagem_saturacao_aumentada

# Função para identificar a cor dominante de um objeto na zona de interesse
def identificar_cor_zona_interesse(imagem, zona_interesse):
    # Definir zona de interesse (região central da imagem)
    x1, y1, x2, y2 = zona_interesse
    zona_interesse_imagem = imagem[y1:y2, x1:x2]

    # Converter a zona de interesse para o espaço de cores HSV
    hsv = cv2.cvtColor(zona_interesse_imagem, cv2.COLOR_BGR2HSV)

    # Definir intervalos de cor para cada cor possível
    intervalos_cor = {
        'VERMELHO': ([0, 100, 100], [10, 255, 255]),
        'AMARELO': ([20, 100, 100], [30, 255, 255]),
        'AZUL': ([90, 100, 100], [120, 255, 255])
    }

    # Inicializar a área máxima e a cor correspondente
    max_area = 0
    cor_identificada = None

    # Iterar sobre os intervalos de cor e encontrar a cor com a maior área de contorno
    for cor, (min_cor, max_cor) in intervalos_cor.items():
        # Aplicar máscara para a cor de referência
        mascara = cv2.inRange(hsv, np.array(min_cor), np.array(max_cor))
        
        # Encontrar contornos na máscara
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calcular a área total dos contornos
        area_total = sum(cv2.contourArea(contorno) for contorno in contornos)
        
        # Atualizar a cor identificada se a área total for maior
        if area_total > max_area:
            max_area = area_total
            cor_identificada = cor

    return cor_identificada

# Replace the URL with the IP camera's stream URL
url = 'http://192.168.74.60/cam-hi.jpg'

# Definir a largura e a altura da zona de interesse
altura, largura = 400, 100  # Ajuste conforme necessário
margem = 100  # Margem para definir a zona de interesse
x1 = (largura // 2) - (margem // 2)
y1 = (altura // 2) - (margem // 2)
x2 = (largura // 2) + (margem // 2)
y2 = (altura // 2) + (margem // 2)
zona_interesse = (x1, y1, x2, y2)

# Create a VideoCapture object
cap = cv2.VideoCapture(url)

# Check if the IP camera stream is opened successfully
if not cap.isOpened():
    print("Failed to open the IP camera stream")
    exit()

# Read and display video frames
while True:
    # Read a frame from the video stream
    img_resp=urllib.request.urlopen(url)
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    im = cv2.imdecode(imgnp,-1)

    # Aumentar a saturação das cores na imagem
    imagem_saturacao_aumentada = aumentar_saturacao(im)

    # Identificar a cor do cubo na zona de interesse
    cor_cubo = identificar_cor_zona_interesse(imagem_saturacao_aumentada, zona_interesse)

    # Verificar se uma cor foi identificada
    if cor_cubo is not None:
        # Converter a cor identificada para minúsculas
        cor_cubo = cor_cubo.lower()
        
        # Definir cores RGB para cada cor
        cores_rgb = {
            'vermelho': (0, 0, 255),
            'amarelo': (0, 255, 255),
            'azul': (255, 0, 0)
        }
        
        # Definir a cor RGB para a cor identificada
        cor_rgb = cores_rgb[cor_cubo]

        # Converter a cor para maiúsculas para exibição
        cor_cubo_maiuscula = cor_cubo.capitalize()

        # Calcular o centro da zona de interesse
        centro_x = (x1 + x2) // 2
        centro_y = (y1 + y2) // 2

        # Desenhar a bounding box na imagem
        cv2.putText(im, f'CUBO IDENTIFICADO - COR: {cor_cubo_maiuscula}', (centro_x + 150, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor_rgb, 2)
        
        # Enviar a cor identificada para o ESP32
        ser.write(cor_cubo.encode())
        time.sleep(1)  # Pequena pausa para garantir que o dado seja enviado

    else:
        print("Nenhuma cor foi identificada.")

    cv2.imshow('Identificacao de Cubo', im)
    key=cv2.waitKey(5)
    if key==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
ser.close()
