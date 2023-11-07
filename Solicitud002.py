import requests

def hacer_solicitud(url, username, user_agent="ElTontito/1.0"):
    """
    Realiza una solicitud GET a una URL con encabezados personalizados.

    Args:
        url (str): La URL a la que se realizará la solicitud.
        username (str): El nombre de usuario en HackerOne.
        user_agent (str, optional): El valor del encabezado User-Agent.
            Default es "ElTontito/1.0".

    Returns:
        dict: Un diccionario que contiene el contenido de la respuesta y los encabezados, o un mensaje de error.
    """
    headers = {
        "X-Hackerone": username,
        "User-Agent": user_agent
    }

    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()

        return {
            "content": response.text,
            "headers": response.headers
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Error en la solicitud: {e}"}

if __name__ == "__main":
    username = "eltontito"
    url = "https://cashback.visa.com.mx/login"

    resultado = hacer_solicitud(url, username)
    if "error" in resultado:
        print(resultado["error"])
    else:
        print("Solicitud exitosa")
        # Acceder al contenido de la respuesta
        print(resultado["content"])
        # Acceder a los encabezados de respuesta
        print(resultado["headers"])