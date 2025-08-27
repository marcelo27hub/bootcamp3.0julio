#importamos movimientos posibles de movimientos 
from movimientosGyR import movimientos_posibles
#definimos nuestra funcion evaluar gato 
def evaluar_estado(pos_gato, pos_raton):
    #si el gato esta en la posicion del raton es por que el gato le atrapo
    if pos_gato == pos_raton:
        #retornamos un valor muy alto por que es muy bueno para el gato 
        return 1000  # el gato atrapo al raton 
    #ejemplo (gato(1,3)) y (raton(3,1))
    #distancia = abs(1-3) + abs(3-1) = 4
    distancia = abs(pos_gato[0] - pos_raton[0]) + abs(pos_gato[1] - pos_raton[1])
    return -distancia 
     #-4  mientras más lejos el ratón, mejor
#definimos nuestra funcion minimax 

def minimax(pos_gato, pos_raton, profundidad, turno_gato, filas, columnas, tablero):
    #si la profunididad es igual a 0 ya no sigue simulando movimientos a futuro, o si el gato atrapo al raton, caso base de recursividad
    if profundidad == 0 or pos_gato == pos_raton:
        #retorna que tan bueno es este estado para el raton 
        #mientras mas lejos estee el gato del raton menor sera el score (mejor para el raton) 
        #ejemplo evaluar_estado(abs(2,2),(4,4)) = abs(2-4)+abs(2-4)= 4
        return evaluar_estado(pos_gato, pos_raton), pos_raton #esto devuelve, (-4), (4,4) en este estado el raton esta a cuatro pasos del gato 
    #si turno 
    if turno_gato:  # turno del gato
        mejor_valor = float("-inf") ##le ponemos un valor -infinito, significa que cualquier valor que encuentre sera mejor que esto, tambien el gato quiere maximizar la puntuacion kjflds
        # por defecto, si no encuentra nada mejor, se queda donde está
        mejor_mov = pos_gato 
        #llamamos a la función movimientos_posibles para obtener todas las pasiciones a las que el gato puede moverse desde su posición actual
        #recorremos cada una para evaluarlas
        for mov in movimientos_posibles(pos_gato, filas, columnas, tablero): 
            #llamamos recursivamente a minimax, cambiando de turno 
            valor, _ = minimax(mov, pos_raton, profundidad - 1, False, filas, columnas, tablero)
            #evaluamos ese movimiento usando recursión: el siguiente turno será del ratón (turno_gato = False).
            #Reducimos la profundidad en 1, porque ya exploramos un nivel más en el árbol de decisiones
            #valor será la el score de que tan bueno fue ese movimiento paraq el gato 
            if valor > mejor_valor: #si el valor es mejor que mejor_valor
                mejor_valor, mejor_mov = valor, mov #lo guardamos en mejor_valor y si fue un buen movimiento lo guradamos en mejor_mov
        #retornamos el mejor valor y el mejor movimiento        
        return mejor_valor, mejor_mov
    else:  # turno del rató
        mejor_valor = float("inf")  #mejor valor para el raton por que cualquier valor que saque sera bueno para el raton(queremos el minimo)
        mejor_mov = pos_raton #inicializamos el mejor movimiento con la posición actual del ratón
        #Obtenemos todos los movimientos posibles del ratón desde su posición actual.
        for mov in movimientos_posibles(pos_raton, filas, columnas, tablero): 
            #llamamos recursivamente al minimax para evaluar ese movimiento
            #Reducimos la profundidad en 1 porque ya avanzamos un nivel en el árbol de decisiones
            valor, _ = minimax(pos_gato, mov, profundidad - 1, True, filas, columnas, tablero) # valor representa qeu tan malo fue ese movimiento para el raton segun la simsulacion
            #si este movimiento da un puntaje menor (mejor para el ratón, ya que queremos minimizar la puntuación del gato)
            if valor < mejor_valor:
                #y lo guardamos en mejor_valor y en mejor_mov
                mejor_valor, mejor_mov = valor, mov
        #retornamos los mejores valores        
        return mejor_valor, mejor_mov
#definimos la funcion para mover automaticamnete al raton con minimax
def mover_raton_minimax(tablero, pos_raton, pos_gato, filas, columnas, profundidad=4):
    #con parametros de tablero,posicion del raton(fila, columna),posicion del gato, filas, columnas, profundidad
    _, mejor_mov = minimax(pos_gato, pos_raton, profundidad, False, filas, columnas, tablero)# llamamos a minimax para calcular la mejor jugada
    #minimax explora todos los movimientos posibles, evaluando cómo reaccionaría el gato.
    #turno_gato = false
    #ejemplo mejor_mov =  (2,2) y se mueve arriba por que es mejor y el punto lo reemplaza por R
    tablero[pos_raton[0]][pos_raton[1]] = " . " #limpiamos la posicion actual del raton en el tablero
    #Comprobamos que el ratón no se mueva a la posición del gato, porque ahí sería atrapado.
    if mejor_mov != pos_gato:
        #Colocamos la R en la nueva posición del ratón (mejor_mov).
        tablero[mejor_mov[0]][mejor_mov[1]] = " R "
    #Devolvemos la nueva posición del ratón para actualizar la variable pos_raton en el juego principal.
    return mejor_mov