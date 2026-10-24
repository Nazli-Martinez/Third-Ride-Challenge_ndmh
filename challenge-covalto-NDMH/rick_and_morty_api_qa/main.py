# Test-API_Nazli Daniela Martínez Hernández

#Librerías
import requests
import time

# URL base de la API
URL_BASE = "https://rickandmortyapi.com/api/character/"

# Personajes principales(los busque en internet)
personajes = {
    1: "Rick Sanchez",
    2: "Morty Smith",
    3: "Summer Smith",
    4: "Beth Smith",
    5: "Jerry Smith"
}

# Resultados esperados
campos = {
    "id": int,
    "name": str,
    "status": str,
    "species": str,
    "episode": list,
    "origin": dict,
    "location": dict,
    "image": str
}

estados_validos = ["Alive", "Dead", "unknown"]

# Consultar los personajes principales
for id_personaje, nombre_esperado in personajes.items():

    url = URL_BASE + str(id_personaje)

    inicio = time.perf_counter()

    try:
        respuesta = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as error:
        print("\n------------------------------")
        print("Personaje:", nombre_esperado)
        print("Error de conexión:", error)
        continue

    fin = time.perf_counter()
    tiempo_respuesta = (fin - inicio) * 1000

    print("\n------------------------------")
    print("Personaje:", nombre_esperado)
    print("Status code:", respuesta.status_code)
    print(f"Tiempo de respuesta: {tiempo_respuesta:.2f} ms")

    # Validación de código HTTP
    if respuesta.status_code != 200:
        print("Validación HTTP: ERROR")
        print("No se puede procesar el personaje.")
        continue

    print("Validación HTTP: CORRECTO")

    # Validación que la respuesta sea JSON válido
    try:
        datos = respuesta.json()
    except requests.exceptions.JSONDecodeError:
        print("Validación JSON: ERROR")
        print("La respuesta no contiene un JSON válido.")
        continue

    # Validación de identidad del personaje
    if (
        datos.get("id") == id_personaje
        and datos.get("name") == nombre_esperado
    ):
        print("Validación de identidad: CORRECTO")
    else:
        print("Validación de identidad: ERROR")
        print("Se recibió un personaje diferente al esperado.")
        continue

    # Validación del estado del personaje
    estado = datos.get("status")

    if estado not in estados_validos:
        print("Validación de estado: ERROR")
        print("El estado recibido no es válido.")
        continue
    elif estado == "Alive":
        print("Estado: VIVO")
    elif estado == "Dead":
        print("Estado: MUERTO")
    else:
        print("Estado: DESCONOCIDO")

    # Mostrar personajes vivos
    if estado != "Alive":
        print("Personaje omitido porque no está vivo.")
        continue
    print("\nPERSONAJE PRINCIPAL VIVO")
    print("Nombre:", datos.get("name"))

    # Validación tipos de datos del response
    print("\nValidación de tipos de datos:")

    for campo, tipo_esperado in campos.items():
        valor = datos.get(campo)

        if isinstance(valor, tipo_esperado):
            print(f"{campo}: CORRECTO")
        else:
            print(
                f"{campo}: ERROR - tipo incorrecto "
                f"(se esperaba {tipo_esperado.__name__})"
            )
