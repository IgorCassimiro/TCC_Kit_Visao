import torch
import torch.nn as nn
from torchvision import transforms
import cv2
import urllib.request
import numpy as np
import serial
import time

# Configurar a comunicação serial
ser = serial.Serial('COM5', 9600)  # Altere 'COM5' para a porta serial correta

# Definir a arquitetura da rede neural conforme o primeiro código
class ColorClassifier(nn.Module):
    def __init__(self):
        super(ColorClassifier, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, 1)
        self.conv2 = nn.Conv2d(16, 32, 3, 1)
        self.fc1 = nn.Linear(32 * 6 * 6, 128)
        self.fc2 = nn.Linear(128, 4)  # 4 classes: azul, amarelo, vermelho, none

    def forward(self, x):
        x = nn.ReLU()(self.conv1(x))
        x = nn.MaxPool2d(2)(x)
        x = nn.ReLU()(self.conv2(x))
        x = nn.MaxPool2d(2)(x)
        x = x.view(-1, 32 * 6 * 6)
        x = nn.ReLU()(self.fc1(x))
        x = self.fc2(x)
        return x

# Carregar o modelo treinado
model = ColorClassifier()
model.load_state_dict(torch.load('best_model.pth'))
model.eval()

# Transformação para pré-processar a imagem
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# Função para identificar a cor usando a rede neural
def identificar_cor_neural(imagem):
    # Pré-processar a imagem diretamente
    imagem_transformada = transform(imagem)#.unsqueeze(0)  # Adicionar dimensão de batch

    # Passar a imagem pela rede neural
    with torch.no_grad():
        outputs = model(imagem_transformada)
    softmax_outputs = torch.softmax(outputs, dim=1)
    max_prob, predicted = torch.max(softmax_outputs, 1)

    print(softmax_outputs)

    # Verificar se a probabilidade da classe prevista é maior que...
    if max_prob.item() > 0.5:
        # Mapear o índice para a cor correspondente
        classes = ['amarelo', 'azul', 'none', 'vermelho']
        cor_identificada = classes[predicted[0].item()]
    else:
        cor_identificada = 'none'

    return cor_identificada

# URL da câmera IP
url = 'http://192.168.133.60/cam-hi.jpg'

# Definir a largura e a altura da zona de interesse
altura, largura = 400, 300  # Ajuste conforme necessário
margem = 200  # Margem para definir a zona de interesse
x1 = (largura // 2) - (margem // 2)
y1 = (altura // 2) - (margem // 2)
x2 = (largura // 2) + (margem // 2)
y2 = (altura // 2) + (margem // 2)
zona_interesse = (x1, y1, x2, y2)

# Loop de captura de vídeo e inferência em tempo real
while True:
    try:
        # Leitura do frame
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        im = cv2.imdecode(imgnp, cv2.IMREAD_COLOR)
        #print(im)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        # Definir a zona de interesse (região central da imagem)
        roi = im[y1:y2, x1:x2]
        #import time
        #timestr = time.strftime("%Y%m%d-%H%M%S")
        #cv2.imwrite(str(timestr)+'.jpg',roi)
        #time.sleep(1)
        # Identificar a cor do cubo na imagem usando a rede neural
        cor_cubo = identificar_cor_neural(roi)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        # Exibir a cor identificada
        if cor_cubo != 'none':
            print(f'Cubo identificado: {cor_cubo}')
            ser.write(cor_cubo.encode())
            time.sleep(1)  # Pequena pausa para garantir que o dado seja enviado
        else:
            print("Nenhuma cor foi identificada.")

        # Mostrar o frame com a cor identificada
        cv2.putText(im, f'Cor: {cor_cubo}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        #im = cv2.rectangle(im, (x1,y1), (x2,y2), (0,255,0), 1)

        cv2.imshow('Identificacao de Cubo', im)
        if cv2.waitKey(1) == ord('q'):
            break
    except Exception as e:
        print(f"Erro ao processar o frame: {e}")
        break

cv2.destroyAllWindows()
ser.close()

