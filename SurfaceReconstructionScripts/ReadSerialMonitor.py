import serial

# Define a porta serial e a taxa de transmissão (baud rate) correspondentes às configurações do Arduino
port = 'COM3'  # Mude para a porta correta (por exemplo, '/dev/ttyUSB0' no Linux)
baud_rate = 115200

# Inicializa a conexão serial
ser = serial.Serial(port, baud_rate)
try:
    while True:
        # Leia uma linha da porta serial
        line = ser.readline().decode('utf-8').strip()
        with open("C:\\Users\\Bruno\\Documents\\TCC\\Software\\EspData.txt", "a") as file:
            file.write(line + "\n")

        # Imprima a linha lida
        print("Dados recebidos:", line)
except KeyboardInterrupt:
    # Encerre a conexão serial se o usuário pressionar Ctrl+C
    ser.close()
    print("Conexão serial encerrada.")