
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

        # Seleccionar la casilla obligatoria de términos
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

        # Volver a consultar el estado de la casilla
        terms = driver.find_element(By.ID, "termsAccepted")

        print(
            "Casilla de términos seleccionada:",
            terms.is_selected()
        )

        # Comprobar el botón sin pulsarlo
        boton = wait.until(
            EC.presence_of_element_located(
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

        print("\nFormulario completado.")
        print("La cuenta NO se ha enviado ni creado.")

        input(
            "Revisa Chrome. Presiona ENTER para cerrar..."
        )

    except Exception as error:
        print(f"ERROR: {type(error).__name__}: {error}")
        input("Presiona ENTER para cerrar el navegador...")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
