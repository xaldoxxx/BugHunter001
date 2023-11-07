import requests

def hacer_solicitud(url, username):
    # Crear un diccionario con los encabezados personalizados
    headers = {
        "X-Hackerone": username,
        "User-Agent": "ElTontito/1.0"  # Reemplaza "MiUserAgent/1.0" con el User-Agent que desees.
    }

    try:
        # Realizar la solicitud GET con los encabezados personalizados
        response = requests.get(url, headers=headers)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            return response.text  # Devuelve el contenido de la respuesta si es necesario
        else:
            return f"La solicitud no fue exitosa. Código de estado: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Error en la solicitud: {e}"

if __name__ == "__main":
    username = "eltontito"
    url = "https://cashback.visa.com.mx/login"

    resultado = hacer_solicitud(url, username)
    print(resultado)
    print(resultado.content)  # Agregamos esta línea para imprimir el contenido de la respuesta.
