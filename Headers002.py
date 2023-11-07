#Configuración de encabezados HTTP inadecuada
import urllib.request
import http.client

class HTTPHeaderChecker:
    def __init__(self, url):
        self.url = url

    def check_http_headers(self):
        try:
            # Realiza una solicitud HEAD al servidor para obtener los encabezados de respuesta.
            response = urllib.request.urlopen(self.url)

            # Lista de encabezados que deseas verificar
            headers_to_check = ['Content-Security-Policy', 'X-Frame-Options', 'Server', 'Strict-Transport-Security']

            for header_name in headers_to_check:
                header_value = response.headers.get(header_name)
                if header_value:
                    print(f'Encabezado {header_name}: {header_value}')
                    # Puedes agregar lógica adicional aquí para analizar los encabezados según tus necesidades.

        except urllib.error.URLError as e:
            print(f'Error al conectar al servidor: {e}')
        except http.client.IncompleteRead as e:
            print(f'Error de lectura: {e}')
        except Exception as e:
            print(f'Error inesperado: {e}')

if __name__ == "__main__":
    url = 'https://www.trip.com/'  # Reemplaza con la URL que deseas analizar
    checker = HTTPHeaderChecker(url)
    checker.check_http_headers()
