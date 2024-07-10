import cv2
import numpy as np

def nothing(x):
    pass

# Inicializa a câmera
cap = cv2.VideoCapture(0)

# Cria uma janela para os controles do threshold
cv2.namedWindow('Threshold Control')
cv2.createTrackbar('Lower Hue', 'Threshold Control', 20, 180, nothing)
cv2.createTrackbar('Upper Hue', 'Threshold Control', 30, 180, nothing)
cv2.createTrackbar('Lower Saturation', 'Threshold Control', 100, 255, nothing)
cv2.createTrackbar('Upper Saturation', 'Threshold Control', 255, 255, nothing)
cv2.createTrackbar('Lower Value', 'Threshold Control', 100, 255, nothing)
cv2.createTrackbar('Upper Value', 'Threshold Control', 255, 255, nothing)

while True:
    # Captura frame por frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # Converte a imagem para o espaço de cores HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Obtém os valores do threshold dos trackbars
    lh = cv2.getTrackbarPos('Lower Hue', 'Threshold Control')
    uh = cv2.getTrackbarPos('Upper Hue', 'Threshold Control')
    ls = cv2.getTrackbarPos('Lower Saturation', 'Threshold Control')
    us = cv2.getTrackbarPos('Upper Saturation', 'Threshold Control')
    lv = cv2.getTrackbarPos('Lower Value', 'Threshold Control')
    uv = cv2.getTrackbarPos('Upper Value', 'Threshold Control')
    
    # Define os limites inferior e superior para a cor amarela
    lower_yellow = np.array([lh, ls, lv])
    upper_yellow = np.array([uh, us, uv])
    
    # Cria uma máscara para a cor amarela
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Encontra os contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtra os contornos por área e desenha o maior contorno
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        max_area = cv2.contourArea(max_contour)
        if max_area > 100:  # Define um limite mínimo para a área do contorno
            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f'Area: {max_area:.2f} px', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Mostra o frame original e a máscara
    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)
    
    # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()
