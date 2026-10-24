
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

URL = "https://www.utest.com/signup"

DATOS_PRUEBA = {
    "firstName": "Prueba",
    "lastName": "QA",
    "email": "qa.prueba@example.com",
    "countryId": "Mexico",
    "birthMonth": "January",
    "birthDay": "7",
    "birthYear": "2003"
}

RESULTADOS = []


def registrar_resultado(caso, resultado, detalle):
    RESULTADOS.append((caso, resultado, detalle))
    print(f"\n{caso}: {resultado}")
    print(detalle)


def abrir_formulario(driver, wait):
    driver.get(URL)
    wait.until(
        EC.visibility_of_element_located((By.ID, "firstName"))
    )


def completar_datos(driver):
    # Datos de prueba; no se envía el formulario en estos casos.
    for campo_id in ("firstName", "lastName", "email"):
        campo = driver.find_element(By.ID, campo_id)
        campo.clear()
        campo.send_keys(DATOS_PRUEBA[campo_id])

    for campo_id in (
        "countryId",
        "birthMonth",
        "birthDay",
        "birthYear"
    ):
        elemento = driver.find_element(By.ID, campo_id)
        Select(elemento).select_by_visible_text(
            DATOS_PRUEBA[campo_id]
        )


def guardar_evidencia(driver, nombre):
    driver.save_screenshot(f"evidencia_{nombre}.png")
    print(f"Evidencia guardada: evidencia_{nombre}.png")


def prueba_correo_invalido(driver, wait):
    print("\n--- CP-11: Correo inválido ---")
    abrir_formulario(driver, wait)

    correo = driver.find_element(By.ID, "email")
    correo.send_keys("correo-invalido")

    valido = driver.execute_script(
        "return arguments[0].checkValidity();", correo
    )
    mensaje = driver.execute_script(
        "return arguments[0].validationMessage;", correo
    )

    guardar_evidencia(driver, "CP11_correo_invalido")

    if not valido:
        registrar_resultado(
            "CP-11", "PASS",
            f"El navegador rechazó el formato. Mensaje: {mensaje}"
        )
    else:
        registrar_resultado(
            "CP-11", "FAIL",
            "El navegador no detectó el formato inválido."
        )


def prueba_campos_vacios(driver, wait):
    print("\n--- CP-12: Campos obligatorios vacíos ---")
    abrir_formulario(driver, wait)

    campos = ("firstName", "lastName", "email")
    invalidos = []

    for campo_id in campos:
        campo = driver.find_element(By.ID, campo_id)
        es_obligatorio = campo.get_attribute("required") is not None
        es_valido = driver.execute_script(
            "return arguments[0].checkValidity();", campo
        )

        print(
            f"{campo_id}: obligatorio={es_obligatorio}, "
            f"válido={es_valido}"
        )

        if es_obligatorio and not es_valido:
            invalidos.append(campo_id)

    guardar_evidencia(driver, "CP12_campos_vacios")

    if invalidos:
        registrar_resultado(
            "CP-12", "PASS",
            "Se detectaron campos obligatorios vacíos: "
            + ", ".join(invalidos)
        )
    else:
        registrar_resultado(
            "CP-12", "NO CONCLUYENTE",
            "No se detectaron campos obligatorios inválidos "
            "entre los campos revisados."
        )


def prueba_fecha_incompleta(driver, wait):
    print("\n--- CP-13: Fecha de nacimiento incompleta ---")
    abrir_formulario(driver, wait)

    anio = Select(driver.find_element(By.ID, "birthYear"))
    opcion_vacia = any(
        opcion.get_attribute("value") == ""
        for opcion in anio.options
    )

    if not opcion_vacia:
        guardar_evidencia(driver, "CP13_fecha")
        registrar_resultado(
            "CP-13", "NO CONCLUYENTE",
            "El selector de año no ofrece una opción vacía. "
            "Se necesita revisar otra restricción de fecha."
        )
        return

    anio.select_by_value("")

    campo = driver.find_element(By.ID, "birthYear")
    valido = driver.execute_script(
        "return arguments[0].checkValidity();", campo
    )
    mensaje = driver.execute_script(
        "return arguments[0].validationMessage;", campo
    )

    guardar_evidencia(driver, "CP13_fecha")

    if not valido:
        registrar_resultado(
            "CP-13", "PASS",
            f"El año vacío fue rechazado. Mensaje: {mensaje}"
        )
    else:
        registrar_resultado(
            "CP-13", "FAIL",
            "El campo de año no detectó el valor vacío."
        )


def prueba_terminos_sin_aceptar(driver, wait):
    print("\n--- CP-14: Términos sin aceptar ---")
    abrir_formulario(driver, wait)
    completar_datos(driver)

    terms = driver.find_element(By.ID, "termsAccepted")

    # Asegurarse de que la casilla quede desmarcada.
    if terms.is_selected():
        driver.execute_script("arguments[0].click();", terms)

    terms = driver.find_element(By.ID, "termsAccepted")
    seleccionado = terms.is_selected()

    # Revisar validez de la casilla, no de todo el formulario,
    # porque otros campos podrían afectar la validez general.
    valido = driver.execute_script(
        "return arguments[0].checkValidity();", terms
    )

    guardar_evidencia(driver, "CP14_terminos")

    if not seleccionado and not valido:
        registrar_resultado(
            "CP-14", "PASS",
            "La casilla sin aceptar se detecta como inválida."
        )
    elif not seleccionado and valido:
        registrar_resultado(
            "CP-14", "NO CONCLUYENTE",
            "La casilla está desmarcada, pero el navegador "
            "no la considera inválida. Se debe comprobar "
            "el comportamiento de la aplicación."
        )
    else:
        registrar_resultado(
            "CP-14", "FAIL",
            "La casilla terminó seleccionada."
        )


def prueba_correo_duplicado(driver, wait):
    print("\n--- CP-15: Correo ya registrado ---")
    abrir_formulario(driver, wait)

    correo = input(
        "Introduce el correo que ya registraste en uTest: "
    ).strip()

    if not correo:
        registrar_resultado(
            "CP-15", "NO EJECUTADO",
            "No se proporcionó un correo para la prueba."
        )
        return

    # Usar los datos de prueba y sustituir solo el correo.
    datos_originales = DATOS_PRUEBA["email"]
    DATOS_PRUEBA["email"] = correo

    try:
        completar_datos(driver)
    finally:
        DATOS_PRUEBA["email"] = datos_originales

    terms = driver.find_element(By.ID, "termsAccepted")

    guardar_evidencia(driver, "CP15_antes_del_envio")

    print(
        "\nEsta prueba enviará el formulario y puede provocar "
        "un nuevo correo o una respuesta del servidor."
    )
    print(
        "Revisa los datos y acepta los términos manualmente "
        "en Chrome solo si estás de acuerdo."
    )

    confirmacion = input(
        "Escribe ENVIAR para confirmar el intento de registro: "
    ).strip()

    if confirmacion != "ENVIAR":
        registrar_resultado(
            "CP-15", "NO EJECUTADO",
            "El envío fue cancelado por el usuario."
        )
        return

    terms = driver.find_element(By.ID, "termsAccepted")

    if not terms.is_selected():
        registrar_resultado(
            "CP-15", "NO EJECUTADO",
            "La casilla de términos no está aceptada."
        )
        return

    boton = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Create Account')]"
            )
        )
    )

    boton.click()
    time.sleep(5)

    texto = driver.find_element(By.TAG_NAME, "body").text
    texto_min = texto.lower()

    print("\nRespuesta visible de uTest:")
    print(texto[:2000])

    guardar_evidencia(driver, "CP15_respuesta")

    indicadores = (
        "already registered",
        "already exists",
        "email already",
        "already in use",
        "ya está registrado",
        "ya existe",
        "correo ya está en uso"
    )

    if any(indicador in texto_min for indicador in indicadores):
        registrar_resultado(
            "CP-15", "PASS",
            "La página mostró un mensaje que indica "
            "que el correo ya está registrado."
        )
    else:
        registrar_resultado(
            "CP-15", "NO CONCLUYENTE",
            "No se identificó un mensaje explícito de correo "
            "duplicado. Revisa el texto y la captura guardada."
        )


def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)

    try:
        driver.maximize_window()

        pruebas = [
            ("CP-11", prueba_correo_invalido),
            ("CP-12", prueba_campos_vacios),
            ("CP-13", prueba_fecha_incompleta),
            ("CP-14", prueba_terminos_sin_aceptar),
            ("CP-15", prueba_correo_duplicado)
        ]

        for caso, funcion in pruebas:
            print(f"\n{'=' * 45}")
            print(f"Ejecutando {caso}")
            print("=" * 45)

            try:
                funcion(driver, wait)
            except Exception as error:
                guardar_evidencia(driver, f"{caso}_error")
                registrar_resultado(
                    caso, "ERROR",
                    f"{type(error).__name__}: {error}"
                )

            if caso != "CP-15":
                input(
                    "\nPresiona ENTER para pasar "
                    "al siguiente caso de prueba..."
                )

        print("\n\n========== RESUMEN DE PRUEBAS ==========")

        for caso, resultado, detalle in RESULTADOS:
            print(f"{caso}: {resultado} - {detalle}")

        print("\nTotal de casos ejecutados:", len(RESULTADOS))

        input("\nPresiona ENTER para cerrar Chrome...")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
