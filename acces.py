import mariadb
from datetime import datetime
from mfrc522 import SimpleMFRC522
lector = SimpleMFRC522()
import RPi.GPIO as GPIO
import time
import os
def clear():
    os.system('clear')
clear()

interruptor = 1
while interruptor == 1:

    # Establir la connexió amb la DB
    conex = mariadb.connect(
        host="localhost",
        user="**********",
        password="**********",
        database="**********"
    )

    # Crear un cursor per executar les consultes
    cursor = conex.cursor()

    # Llegira el nombre de xip i el posara dins la variable UID
    UID, text = lector.read() #Lector.read inicia el lector RFID

    data = datetime.now().date()  # Obtenir la data actual
    hora = datetime.now().time()  # Obtenir l' hora actual

    # Registra la consulta per a afegir una acces amb el nombre del xip i fecha i hora a la que s'ha passat
    consulta = "INSERT INTO Acces (UID, Data, Hora) VALUES (%s, %s, %s)"
    dades = (UID, data, hora)

    try:
        cursor.execute(consulta, dades) # Executar la consulta
        print(f"Acces registrat de {UID}")
        time.sleep(2)
        clear()

        # Guardar els canvis
        conex.commit()

    except mariadb.Error as e:
        print(f"Error al agregar el acceso: {e}")
