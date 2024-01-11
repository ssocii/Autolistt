import mariadb
import os
import time
from mfrc522 import SimpleMFRC522
lector = SimpleMFRC522()
import RPi.GPIO as GPIO
def clear():
    os.system('clear')
clear()

interruptor = 1
while interruptor == 1:

    try:
        # Credencials per iniciar conexió amb la DB
        conex = mariadb.connect(
            host="localhost",
            user="auto",
            password="Autoli.23",
            database="autolistt"
        )
        # Crear un cursor per poder executar les consultes
        cursor = conex.cursor() # Estableix una conexió amb la DB

    except mariadb.Error as e: # En cas de no poder executar la consulta ens donara un missatge d'error
        clear()
        print(f"Error en la conexió a la base de dades: {e}")
        interruptor = 2

    # Menú que ens ensenyara les possibles opcions que podem realitzar en el programa
    clear()
    print('         ACCIONS             ')
    print('-----------------------------')
    print('| 1-Consultar acces per dia |')
    print('| 2-Consultar alumne        |')
    print('| 3-Tancar programa         |')
    print('-----------------------------')

    accio = int(input('Quina acció desitges realitzar? '))
    clear()

    if accio == 1:
        clear()
        data = input("Introdueix 'YYYY-MM-DD' que vulguis consultar: ")

        try:
            # Executa la consulta
            cursor.execute("SELECT nom_llinatges, Data FROM Alumnat, Acces WHERE Alumnat.UID = Acces.UID AND Data = ?", (data,))

            # Ens mostra els resulats
            resultados = cursor.fetchall()
            for resultado in resultados:
                print(resultado)
                
            # Tanca el cursor i la connexió
            cursor.close()
            conex.close()
            input ("Presiona la tecla 'Enter' per continuar...")
            clear()

        except mariadb.Error as e: # Mostrarà un error en cas d'error en la consulta
            print(f"Error en la sel·leció per data: {e}")

    elif accio == 2: # Mostrar la infromació d'un alumne
        print("Posa el xip damunt del lector")
        UID, text = lector.read()
    
        # Consulta SQL per a sel·leccionar informació de l'aulmne que coincideixi amb el número de xip
        consulta = "SELECT * FROM Alumnat WHERE UID=%s"
        dades = (UID,)

        try:
            clear()
            # Executa la consulta
            cursor.execute(consulta, dades)

            # Ens mostra els resulats
            print("Informació de l'alumne amb UID " + str(UID))
            print("")
            resultats = cursor.fetchall()
            for info in resultats:
                print(info)
                print("")
                print("")
                input("Presiona la tecla 'Enter' per continuar...")
                clear()
            
            # Tanca el cursor i la connexió
            cursor.close()
            conex.close()

        except mariadb.Error as e: # Mostrarà un error en cas d'error en la consulta
            print(f"Error en la sel·lecció de l'alumne: {e}")

    elif accio == 3:
        clear()
        print("Tancant el programa...")
        time.sleep(2)
        clear()

    else:
        print("L'opció triada no coincideix amb cap del menú.")
