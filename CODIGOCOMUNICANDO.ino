#include <Arduino.h>
#include <ESP32Servo.h>

Servo Garra, BaseGarra, Giro;  // cria um objeto Servo para a Garra

int pos = 0;    // variável para armazenar a posição do servo
// Pinos GPIO PWM recomendados no ESP32 incluem 2,4,12-19,21-23,25-27,32-33 
int pinServoGarra = 12; 
int pinServoGira = 5; 
int pinServoBase = 19; 

#define DIR_PIN  14  // Pino para controle da direção do motor
#define STEP_PIN 27  // Pino para controle do passo do motor
#define STEP_DELAY 820  // Ajuste esse valor para controlar a velocidade do motor

const int sensorPin = 4; // Pino ao qual o sensor está conectado
int motorPin = 26; // Pino ao qual o motor está conectado

volatile bool detectado = false;
String corCubo = "";

void sensorTask(void * parameter) {
  (void)parameter;
  
  pinMode(sensorPin, INPUT_PULLUP); // Configura o pino do sensor como entrada com pull-up interno
  
  for (;;) {
    int sensorValue = digitalRead(sensorPin); // Lê o valor do sensor
    if (sensorValue == LOW) { // Se o sensor detectar reflexão
      detectado = true;
      Serial.println("Detectado");
    } else {
      detectado = false;
      Serial.println("Não Detectado");
    }
    delay(100); // Pequena pausa para estabilidade
  }
}

void motorTask(void * parameter) {
  (void)parameter;
  
  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(motorPin, OUTPUT); // Configura o pino do motor como saída
  
  for (;;) {
    if (!detectado) { // Se não houver detecção do sensor
      digitalWrite(DIR_PIN, LOW);  // Define a direção do motor (HIGH para uma direção, LOW para a outra)
      
      // Gira o motor continuamente em uma direção
      digitalWrite(STEP_PIN, HIGH);
      delayMicroseconds(STEP_DELAY);
      digitalWrite(STEP_PIN, LOW);
      delayMicroseconds(STEP_DELAY);
    } else {
      // Para o motor
      digitalWrite(STEP_PIN, LOW);
      
      // Executa a sequência da garra com base na cor detectada
      if (corCubo == "vermelho") {
        // Movimento para a direita
        Garra.write(32); delay(500);
        BaseGarra.write(100);  delay(1000);
        Giro.write(90); delay(2000);
        BaseGarra.write(19);  delay(2000);
        Garra.write(110); delay(500);
        BaseGarra.write(100);  delay(1000);
        Giro.write(0); delay(500);
        BaseGarra.write(19);  delay(1000);
        Garra.write(32);
      } else if (corCubo == "amarelo") {
        // Movimento para o centro
        Garra.write(32); delay(500);
        BaseGarra.write(100);  delay(1000);
        Giro.write(90); delay(2000);
        BaseGarra.write(19);  delay(2000);
        Garra.write(110); delay(500);
        BaseGarra.write(180);  delay(1000);
        Garra.write(32);
      } else if (corCubo == "azul") {
        // Movimento para a esquerda
        Garra.write(32); delay(500);
        BaseGarra.write(100);  delay(1000);
        Giro.write(90); delay(2000);
        BaseGarra.write(19);  delay(2000);
        Garra.write(110); delay(500);
        BaseGarra.write(100);  delay(1000);
        Giro.write(180); delay(500);
        BaseGarra.write(19);  delay(1000);
        Garra.write(32);
      }
      
      detectado = false; // Reseta a variável de detecção
    }
    
    if (Serial.available() > 0) {
      corCubo = Serial.readString();
      Serial.println("Cor recebida: " + corCubo);
    }
  }
}

void setup() {
  Serial.begin(9600);
  
  Garra.attach(pinServoGarra); // Anexa o servo ao pino correspondente
  BaseGarra.attach(pinServoBase); // Anexa o servo ao pino correspondente
  Giro.attach(pinServoGira);
  
  xTaskCreatePinnedToCore(sensorTask, "Sensor Task", 10000, NULL, 1, NULL, 0);
  xTaskCreatePinnedToCore(motorTask, "Motor Task", 10000, NULL, 1, NULL, 1);
}

void loop() {
  // nothing to do here
}
