
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.utest.com/signup"

DATOS = {
    "firstName": "Nazli",
    "lastName": "Martinez",
    "email": "ndmh713@gmail.com",
    "countryId": "Mexico",
    "birthMonth": "January",
    "birthDay": "7",
    "birthYear": "2003"
}


def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)

    try:
        driver.maximize_window()
        driver.get(URL)

        # Esperar a que cargue el formulario
        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "firstName")
            )
        )

        print("PASS: Formulario cargado.")

        # Completar nombre, apellido y correo
        for campo_id in ("firstName", "lastName", "email"):
            campo = wait.until(
                EC.visibility_of_element_located(
                    (By.ID, campo_id)
                )
            )

            campo.clear()
            campo.send_keys(DATOS[campo_id])

            print(f"PASS: {campo_id} completado.")

        # Seleccionar país y fecha de nacimiento
        for campo_id in (
            "countryId",
            "birthMonth",
            "birthDay",
            "birthYear"
        ):
            elemento = wait.until(
                EC.presence_of_element_located(
                    (By.ID, campo_id)
                )
            )

            Select(elemento).select_by_visible_text(
                DATOS[campo_id]
            )

            print(f"PASS: {campo_id} seleccionado.")

        # Seleccionar la casilla de términos
        terms = wait.until(
            EC.presence_of_element_located(
                (By.ID, "termsAccepted")
            )
        )

        if not terms.is_selected():
            driver.execute_script(
                "arguments[0].click();",
                terms
            )

        terms = driver.find_element(
            By.ID, "termsAccepted"
        )

        print(
            "Casilla de términos seleccionada:",
            terms.is_selected()
        )

        if not terms.is_selected():
            raise Exception(
                "No se pudo seleccionar la casilla de términos."
            )

        # Comprobar el botón Create Account
        boton = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(., 'Create Account')]"
                )
            )
        )

        print(
            "Botón Create Account habilitado:",
            boton.is_enabled()
        )

        # Guardar evidencia antes de enviar
        driver.save_screenshot(
            "evidencia_registro_completado.png"
        )

        print(
            "Captura guardada: "
            "evidencia_registro_completado.png"
        )

        # Confirmar el envío
        input(
            "\nRevisa los datos en Chrome. "
            "Presiona ENTER para enviar el registro..."
        )

        # Volver a localizar el botón y hacer clic
        boton = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(., 'Create Account')]"
                )
            )
        )

        boton.click()

        print("\nSe hizo clic en Create Account.")

        # Esperar una posible respuesta o cambio de página
        try:
            wait.until(
                lambda d: (
                    d.current_url != URL
                    or d.find_element(
                        By.TAG_NAME, "body"
                    ).text.strip() != ""
                )
            )
        except Exception:
            print(
                "AVISO: No se detectó un cambio "
                "claro en la página."
            )

        # Dar tiempo a que termine de actualizarse
        import time
        time.sleep(3)

        # Mostrar el resultado
        print("\n--- RESULTADO DEL REGISTRO ---")
        print("URL actual:", driver.current_url)
        print("Título:", driver.title)

        texto_pagina = driver.find_element(
            By.TAG_NAME, "body"
        ).text

        print("\nTexto visible de la página:")
        print(texto_pagina[:2500])

        # Guardar evidencia después del envío
        driver.save_screenshot(
            "evidencia_registro_enviado.png"
        )

        print(
            "\nCaptura guardada: "
            "evidencia_registro_enviado.png"
        )

        print(
            "\nRevisa el mensaje de uTest para confirmar "
            "si el registro fue aceptado."
        )

        input(
            "Revisa Chrome. Presiona ENTER para cerrar..."
        )

    except Exception as error:
        print(
            f"ERROR: {type(error).__name__}: {error}"
        )

        try:
            driver.save_screenshot(
                "evidencia_registro_error.png"
            )
            print(
                "Captura guardada: "
                "evidencia_registro_error.png"
            )
        except Exception:
            pass

        input(
            "Presiona ENTER para cerrar el navegador..."
        )

    finally:
        driver.quit()


if __name__ == "__main__":
    main()

