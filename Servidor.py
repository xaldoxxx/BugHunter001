# Información de versión del servidor

import requests

class ServerVersionChecker:
    def __init__(self, url):
        self.url = url

    def check_server_version(self):
        try:
            response = requests.get(self.url)
            server_header = response.headers.get('Server')

            if server_header:
                print(f'Versión del servidor: {server_header}')
                # Aquí puedes agregar lógica para verificar si la versión del servidor es vulnerable.
                # Por ejemplo, puedes comparar la versión con una lista de versiones conocidas con vulnerabilidades.

            else:
                print('El servidor no proporciona información de versión.')

        except requests.exceptions.RequestException as e:
            print(f'Error al conectarse al servidor: {e}')

if __name__ == "__main__":
    url = 'https://www.trip.com/'  # Reemplaza con la URL que deseas analizar
    checker = ServerVersionChecker(url)
    checker.check_server_version()