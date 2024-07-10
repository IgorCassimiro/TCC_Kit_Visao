import cv2
import numpy as np
import matplotlib.pyplot as plt

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

def select_roi_and_show_histogram(image_path):
    # Carregar a imagem
    image = cv2.imread(image_path)
    if image is None:
        print("Erro ao carregar a imagem.")
        return

    # Aumentar a saturação das cores na imagem
    image_saturada = aumentar_saturacao(image)

    # Converter a imagem original para HSV
    image_hsv = cv2.cvtColor(image_saturada, cv2.COLOR_BGR2HSV)

    # Mostrar a imagem e permitir que o usuário selecione uma ROI
    roi = cv2.selectROI("Selecione a Região de Interesse", image_saturada)
    cv2.destroyAllWindows()

    # Verificar se uma região foi selecionada
    if roi == (0, 0, 0, 0):
        print("Nenhuma região selecionada.")
        return

    # Cortar a região de interesse da imagem
    x, y, w, h = roi
    roi_cropped_hsv = image_hsv[y:y+h, x:x+w]

    # Preparar a figura para os subplots
    plt.figure(figsize=(12, 8))

    # Subplot da imagem original
    plt.subplot(2, 4, 1)
    plt.imshow(cv2.cvtColor(image_saturada, cv2.COLOR_BGR2RGB))
    plt.title("Imagem Saturada")
    plt.axis('off')

    # Subplot do histograma do canal H da imagem original em HSV
    plt.subplot(2, 4, 2)
    plt.title("Histograma de H (Imagem Original)")
    plt.xlabel("Valor de H")
    plt.ylabel("Quantidade de pixels")
    hist_h = cv2.calcHist([image_hsv], [0], None, [256], [0, 256])
    plt.plot(hist_h, color='r')
    plt.xlim([0, 256])

    # Subplot do histograma do canal S da imagem original em HSV
    plt.subplot(2, 4, 3)
    plt.title("Histograma de S (Imagem Original)")
    plt.xlabel("Valor de S")
    plt.ylabel("Quantidade de pixels")
    hist_s = cv2.calcHist([image_hsv], [1], None, [256], [0, 256])
    plt.plot(hist_s, color='g')
    plt.xlim([0, 256])

    # Subplot do histograma do canal V da imagem original em HSV
    plt.subplot(2, 4, 4)
    plt.title("Histograma de V (Imagem Original)")
    plt.xlabel("Valor de V")
    plt.ylabel("Quantidade de pixels")
    hist_v = cv2.calcHist([image_hsv], [2], None, [256], [0, 256])
    plt.plot(hist_v, color='b')
    plt.xlim([0, 256])

    # Subplot da região selecionada
    plt.subplot(2, 4, 5)
    plt.imshow(cv2.cvtColor(roi_cropped_hsv, cv2.COLOR_HSV2RGB))
    plt.title("Região Selecionada")
    plt.axis('off')

    # Subplot do histograma do canal H da região selecionada em HSV
    plt.subplot(2, 4, 6)
    plt.title("Histograma de H (Região Selecionada)")
    plt.xlabel("Valor de H")
    plt.ylabel("Quantidade de pixels")
    hist_h_roi = cv2.calcHist([roi_cropped_hsv], [0], None, [256], [0, 256])
    plt.plot(hist_h_roi, color='r')
    plt.xlim([0, 256])

    # Subplot do histograma do canal S da região selecionada em HSV
    plt.subplot(2, 4, 7)
    plt.title("Histograma de S (Região Selecionada)")
    plt.xlabel("Valor de S")
    plt.ylabel("Quantidade de pixels")
    hist_s_roi = cv2.calcHist([roi_cropped_hsv], [1], None, [256], [0, 256])
    plt.plot(hist_s_roi, color='g')
    plt.xlim([0, 256])

    # Subplot do histograma do canal V da região selecionada em HSV
    plt.subplot(2, 4, 8)
    plt.title("Histograma de V (Região Selecionada)")
    plt.xlabel("Valor de V")
    plt.ylabel("Quantidade de pixels")
    hist_v_roi = cv2.calcHist([roi_cropped_hsv], [2], None, [256], [0, 256])
    plt.plot(hist_v_roi, color='b')
    plt.xlim([0, 256])

    plt.tight_layout()
    plt.show()


# Cor Azul
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Azul1.png")
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Azul2.png")
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Azul3.png")
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Azul4.png")
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Azul5.png")
# Cor Vermelha
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Vermelho1.png")
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Vermelho2.png")
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Vermelho3.png")
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Vermelho4.png")
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Vermelho5.png")
# Cor Amarela
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Amarelo1.png")
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Amarelo2.png")
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Amarelo3.png")
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Amarelo4.png")
select_roi_and_show_histogram(r"C:\Users\igorc\Downloads\Fotos de cubos coloridos Esteira\Amarelo5.png")
