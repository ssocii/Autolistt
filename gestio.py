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
            user="**********",
            password="*********",
            database="*********"
        )
        # Creació d'un cursor per poder executar les consultes
        cursor = conex.cursor() # Estableix una conexió amb la DB

    except mariadb.Error as e: # En cas de no poder establir amb una connexió ens mostrarà un error
        clear()
        print(f"Error en la conexió a la base de dades: {e}")
        interruptor = 2

    # Menú que ens ensenyara les possibles opcions que podem realitzar en el programa
    print('         ACCIONS         ')
    print('-------------------------')
    print('| 1-Nou alumne          |')
    print('| 2-Consultar alumne    |')
    print('| 3-Borrar un alumne    |')
    print('| 4-Tancar programa     |')
    print('-------------------------')

    accio = int(input('Quina acció desitges realitzar? '))
    clear()

    if accio == 1: # La opció número 1 es per registrar un nou alumne a la base de dades

        # Demanar el número de xip i informació sobre l'alumne        
        print("Posa el nou xip damunt del lector")
        UID, text = lector.read()
        clear()
        print("Número de xip: " + str(UID))
        nom = input("Introdueix nom i llinatges de l'alumne: ")
        dni = input("Introdueix DNI de l'alumne: ")
        correu = input("Correu corporatiu de l'alumne: ")
        numtel = input("Número de telèfon: ")
        neixament = input("Data neixament alumne: ")
        cicle = input("Cicle formatiu: ")

        # Consulta SQL per insertar la informació anterior a la taula "Alumnat"
        consulta = "INSERT INTO `Alumnat` (`UID`, `nom_llinatges`,`DNI`, `c_electronic`, `num_tel`, `d_neixament`, `c_formatiu`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        dades = (UID, nom, dni, correu, numtel, neixament, cicle)

        try:
            # Executa la consulta
            cursor.execute(consulta, dades)

            # Guarda el canvis
            conex.commit()

            # Tanca el cursos i la conexió
            cursor.close()
            conex.close()

            clear()

        except mariadb.Error as e: # En cas de no poder executar la consulta ens donara un missatge d'error
            print(f"Error en la creació d'un nou alumne: {e}")

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
        print("Posa el xip damunt del lector")
        UID, text = lector.read()
    
        # Consulta SQL per a borrar un alumne, també es borrarán tots els seus accesos
        consulta = "DELETE FROM Alumnat WHERE UID=%s"
        dades = (UID,)

        try:
            # Executar la consulta
            cursor.execute(consulta, dades)

            # Guardar els canvis
            conex.commit()

            # Tancar el cursor i la conexió
            cursor.close()
            conex.close()
            clear()
        
        except mariadb.Error as e: # En cas de que no s'executi bé la consulta ens donarà un error
            print(f"Error al borrar un alumne: {e}")

    elif accio == 4: # Tanca el programa
        clear()
        print("Tancant el programa...")
        time.sleep(2)
        interruptor = 2
        clear()

    else:
        print("L'opció triada no coincideix amb cap del menú.") 
