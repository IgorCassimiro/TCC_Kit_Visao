#include <ESP32Servo.h>

#define SERVO_PIN 12 // Pino do ESP32 para o servo motor
#define SERVO_MIN_ANGLE 0// Ângulo mínimo de rotação
#define SERVO_MAX_ANGLE 180 // Ângulo máximo de rotação

Servo garra; // Criação de um objeto Servo para controlar o motor

void setup() {
  Serial.begin(9600); // Inicialização da comunicação serial
  garra.attach(SERVO_PIN); // Vincula o objeto Servo ao pino do motor
  pinMode(2, OUTPUT);
}

void loop() {
  // if (Serial.available() > 0) { // Verifica se há dados disponíveis no monitor serial
  //   char comando = Serial.read(); // Lê o comando enviado pelo monitor serial
  //   if (comando == '1') { // Se o comando for '1', movimenta a garra
  //     moverGarra();
  //   } else if (comando == '0') { // Se o comando for '0', para a garra
  //     pararGarra();
  //   }
  // }
   garra.write(118);
   Serial.print("Foi para 110");
   delay(3000);

   garra.write(20);
   Serial.println("Foi para 20");
   delay(3000);
}

void moverGarra() {
  for (int angulo = SERVO_MIN_ANGLE; angulo <= SERVO_MAX_ANGLE; angulo += 1) { // Loop para mover a garra até 180 graus
    garra.write(angulo); // Define a posição do servo motor
    delay(15); // Pequeno atraso para suavizar o movimento
  }
  delay(500); // Pequeno atraso após o movimento completo
}

void pararGarra() {
  for (int angulo = SERVO_MAX_ANGLE; angulo >= SERVO_MIN_ANGLE; angulo -= 1) { // Loop para mover a garra de volta para a posição inicial
    garra.write(angulo); // Define a posição do servo motor
    delay(15); // Pequeno atraso para suavizar o movimento
  }
  delay(500); // Pequeno atraso após o movimento completo
}