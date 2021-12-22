from sympy import *

def puntos_fijos(funcion, parametro):
    #se obtienen los puntos fijos de la funcion en base al "parametro"
    funcion = funcion-x
    p_fijos = solve(funcion, parametro)
    return p_fijos

def iterar(funcion, n):
    #itera la funcion n veces
    f_iterada = funcion
    for i in range(n):
        f_iterada = f_iterada.subs(x, funcion)
    
    return f_iterada

def deriva(funcion, respecto_a):
    #obtener la deriavada de una funcion con respecto a una variable
    f_derivada = diff(funcion, respecto_a)
    return f_derivada

def naturalezas(fun_derivada, soluciones):
    #encuentra las naturalezas de los puntos fijos
    evaluacion = []
    tipos = []

    for i in range(len(soluciones)):
        resultado = fun_derivada.subs(x,soluciones[i])
        evaluacion.append(resultado)

        tipo_repulsor = solve(simplify(abs(resultado))>1)
        if(not tipo_repulsor):
            if abs(resultado) == 1:
                tipos.append("Neutro")
            elif abs(resultado) > 1:
                tipos.append("repulsor")
            elif abs(resultado) < 1:
                tipos.append("atractor")
        else:
            tipo_repulsor = ("es repulsor cuando lambda pertenece al intervalo", tipo_repulsor)
            try:
                tipo_neutro = ("es neutro cuando lambda pertenece al intervalo", solve(simplify(abs(resultado))-1))
            except:
                tipo_neutro = ("es neutro cuando lambda pertenece al intervalo", solve(simplify(resultado)-1))
            
            tipo_atractor = ("es atractor cuando lambda pertenece al intervalo", solve(simplify(abs(resultado))<1))
            tipos.append((tipo_repulsor, tipo_neutro, tipo_atractor))

    return evaluacion, tipos

def encontrar_ciclos(funcion, p_fijos, p_fijos_iterada):
    #encuentra los ciclos (en caso de haberlos) en la funcion iterada
    posibles_ciclos = []
    ciclos = []

    for i in range(len(p_fijos_iterada)):
        try:
            p_fijos.index(p_fijos_iterada[i])
        except:
            posibles_ciclos.append(p_fijos_iterada[i])

    for j in range(len(posibles_ciclos)):
        p_fijo_prueba = posibles_ciclos[j]
        funcion_p_fijo_prueba = funcion.subs(x,p_fijo_prueba)
        funcion_p_fijo_prueba = simplify(funcion_p_fijo_prueba)
        try:
            posible = p_fijos_iterada.index(funcion_p_fijo_prueba)
            ciclos.append(p_fijo_prueba)
        except:
            continue

    return ciclos

def nat_ciclo(fun_derivada, ciclo):
    #obtener la naturaleza del ciclo encontrado en la funcion iterada
    derivada1 = fun_derivada.subs(x,ciclo[0])
    derivada2 = fun_derivada.subs(x,ciclo[1])
    mult_derivadas = abs(derivada1*derivada2)

    atractor = ("es atractor cuando lambda pertenece al intervalo:", solve(simplify(mult_derivadas) < 1))
    neutro = ("es neutro cuando lambda pertenece al intervalo:", solve(simplify(mult_derivadas) - 1))
    repulsor = ("es repulsor cuando lambda pertenece al intervalo", solve(simplify(mult_derivadas) > 1))
    naturaleza_ciclo = (atractor, neutro, repulsor)
    return(naturaleza_ciclo)

def diagrama_bifurcacion(p_fijos):
    #en caso de haber ciclo de longitud 2 se imprime
    #la bifurcacion de doble periodo
    #de lo contrario se imprime los puntos fijos de la primer funcion
    graph = plot(p_fijos[0], show = False)
    for i in range(len(p_fijos)):
        if i != 0:
            p_fijo_plot = plot(p_fijos[i], (2, -50, 50), show = False)
            graph.append(p_fijo_plot[0])
    graph.show()

def proceso(funcion):
    print("su funcion: ", funcion)
    print("formula para encontrar los puntos fijos: ", (str(funcion-x))+" = 0", "\n")

    p_fijos = puntos_fijos(funcion, x)
    print("su(s) punto(s) fijo(s) es/son: ", p_fijos, "\n")

    fun_derivada = deriva(funcion, x)
    print("la derivada de la funcion es: ", fun_derivada, "\n")

    evaluacion, tipo = naturalezas(fun_derivada, p_fijos)
    for i in range(len(evaluacion)):
        print("punto fijo evaluado: ", evaluacion[i], ", su naturaleza: ", tipo[i], "\n")

    #si se desea iterar mas de una vez la funcion, basta con cambiar el valor
    #a la derecha de funcion por el numero de veces que se desea iterar
    fun_iterada = iterar(funcion, 1)
    print("la funcion iterada es: ", fun_iterada, "\n")

    p_fijos_iterada = puntos_fijos(fun_iterada, x)
    print("los puntos fijos de la funcion iterada son: ", p_fijos_iterada, "\n")

    ciclo = encontrar_ciclos(funcion, p_fijos, p_fijos_iterada)
    if len(ciclo) != 0:
        print("ciclo de longitud 2 en la funcion iterada: ", ciclo, "\n")

        naturaleza_ciclo = nat_ciclo(fun_derivada, ciclo)
        print("la naturaleza del ciclo de longitud 2", naturaleza_ciclo)

    else:
        print("no hay bifurcacion de doble periodo")
    
if __name__ == '__main__':
    #Inicio del programa, se definen los simbolos a usar para ser tomados
    #como parametros, en este caso x, y l="lambda"
    x, l = symbols('x l', real=True) #No editar

    #A continuacion se declaran las funciones con las cuales se desea trabajar
    #las dos funciones predefinidas son las sugeridas para probar el programa
    #para ver los resultados de cualquiera de las funciones solo basta con
    #descomentar las lineas de la funcion deseada y comentar el resto
    #para descomentar una linea eliminar el simbolo "#" antes de la linea
    #para comentar una linea agregar el simbolo "#" al inicio de la linea
    
    #Si se desea agregar una nueva funcion existe "f3" para este proposito, esta es la sintaxis a seguir
    #toda lambda debe ser represntada por "l", toda equis por "x"
    #si se tiene una variable/parametro multiplicada por otro valor
    #debe tener un "*" uniendolos para indicar que es una multiplicacion
    #para indicar potencias se hace con "**" por ejemplo "x**3"
    #representa equis al cubo
    #no debe haber espacios

    #f1 = l*x+x**3 
    #proceso(f1)

    #f2 = l*x**3-x**5
    #proceso(f2)

    f3 = l*x+x**3
    proceso(f3)