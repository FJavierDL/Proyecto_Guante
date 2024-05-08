import serial
import time

def config_puerto_serie():
    puerto_serie = serial.Serial('COM3', 115200, xonxoff=True)    # Configurar la comunicación serie
    time.sleep(2)     # Esperar un tiempo para que la comunicación se establezca correctamente
    return puerto_serie