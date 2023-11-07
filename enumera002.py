# directorios
import urllib.request
from urllib.error import HTTPError
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class HTTPDirectoryChecker:
    def __init__(self, base_url, max_depth=3, sensitive_directories=None):
        self.base_url = base_url
        self.max_depth = max_depth
        self.sensitive_directories = sensitive_directories or []

    def check_directory_exposure(self, url, depth=0):
        if depth > self.max_depth:
            return

        try:
            response = urllib.request.urlopen(url)
            if response.status == 200:
                print(f'Página visitada ({depth} niveles): {url}')
                soup = BeautifulSoup(response.read(), 'html.parser')

                for link in soup.find_all('a'):
                    href = link.get('href')
                    full_url = urljoin(url, href)

                    if self.is_sensitive_directory(full_url):
                        print(f'Exposición de directorio sensible encontrado: {full_url}')

                    if depth < self.max_depth and self.is_internal_link(full_url):
                        self.check_directory_exposure(full_url, depth + 1)

        except HTTPError as e:
            if e.code == 404:
                print(f'La página visitada no existe: {url}')
            else:
                print(f'Error al conectar al servidor: {e}')
        except Exception as e:
            print(f'Error inesperado: {e}')

    def is_internal_link(self, full_url):
        return full_url.startswith(self.base_url)

    def is_sensitive_directory(self, full_url):
        return any(directory in full_url for directory in self.sensitive_directories)

if __name__ == "__main__":
    url = 'https://xaldoxxx.com.ar/'  # Reemplaza con la URL que deseas analizar
    sensitive_dirs = ["cpanel", "admin", "secret", "private", "login", "test", ""]  # Lista de directorios sensibles
    checker = HTTPDirectoryChecker(url, max_depth=3, sensitive_directories=sensitive_dirs)
    checker.check_directory_exposure(url)
