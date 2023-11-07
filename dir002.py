# Exposición de directorios
import urllib.request
from urllib.error import HTTPError
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class HTTPDirectoryChecker:
    def __init__(self, base_url):
        self.base_url = base_url
        self.sensitive_directories = ["cpanel", "admin", "secret", "private", "pass", "passwd", "etc"]  # Lista de directorios sensibles

    def check_directory_exposure(self):
        try:
            # Realiza una solicitud GET al URL base.
            response = urllib.request.urlopen(self.base_url)

            if response.status == 200:
                print(f'Página de inicio: {self.base_url}')

                # Parsea el contenido HTML de la página de inicio.
                soup = BeautifulSoup(response.read(), 'html.parser')

                # Busca enlaces en la página de inicio y verifica si corresponden a directorios sensibles.
                for link in soup.find_all('a'):
                    href = link.get('href')
                    full_url = urljoin(self.base_url, href)

                    if any(directory in full_url for directory in self.sensitive_directories):
                        print(f'Exposición de directorio sensible encontrado: {full_url}')

        except HTTPError as e:
            if e.code == 404:
                print(f'La página de inicio no existe: {self.base_url}')
            else:
                print(f'Error al conectar al servidor: {e}')
        except Exception as e:
            print(f'Error inesperado: {e}')

if __name__ == "__main__":
    url = 'https://www.mobile-phantom.com/homepage'  # Reemplaza con la URL que deseas analizar
    checker = HTTPDirectoryChecker(url)
    checker.check_directory_exposure()
