import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor

class AnalizadorInyeccionSQL:
    def __init__(self, url_base, profundidad_maxima=3, hilos_maximos=5):
        """
        Inicializa el Analizador de Inyección SQL.

        Args:
            url_base (str): La URL base a analizar.
            profundidad_maxima (int): La profundidad máxima de análisis.
            hilos_maximos (int): El número máximo de hilos de análisis concurrentes.
        """
        self.url_base = url_base
        self.urls_visitadas = set()
        self.profundidad_maxima = profundidad_maxima
        self.hilos_maximos = hilos_maximos

    def extraer_y_analizar(self, url, profundidad=0):
        """
        Extrae y analiza formularios y enlaces en una URL dada.

        Args:
            url (str): La URL a analizar.
            profundidad (int): La profundidad actual de análisis.
        """
        try:
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                formularios = soup.find_all('form')

                self.urls_visitadas.add(url)

                if formularios:
                    print(f"Analizando URL: {url}")

                for formulario in formularios:
                    accion = formulario.get('action')
                    if accion:
                        url_formulario = urljoin(url, accion)
                        url_parseada = urlparse(url_formulario)

                        if url_parseada.netloc == urlparse(self.url_base).netloc:
                            print(f'Formulario encontrado en {url}')
                            print(f'Acción del formulario: {url_formulario}')
                            print(f'Método del formulario: {formulario.get("method", "GET")}')
                            print('Campos del formulario:')

                            for campo_input in formulario.find_all('input'):
                                nombre_campo = campo_input.get('name')
                                if nombre_campo:
                                    print(f' - {nombre_campo}')

                if profundidad < self.profundidad_maxima:
                    with ThreadPoolExecutor(max_workers=self.hilos_maximos) as executor:
                        futuros = {executor.submit(self.extraer_y_analizar, urljoin(url, enlace.get('href')), profundidad + 1): enlace for enlace in soup.find_all('a') if enlace.get('href')}
                        for futuro in futuros:
                            enlace_futuro = futuros[futuro]
                            try:
                                futuro.result()
                            except requests.exceptions.RequestException as e:
                                print(f'Error al analizar {enlace_futuro}: {e}')
                            except Exception as e:
                                print(f'Error inesperado al analizar {enlace_futuro}: {e}')

        except requests.exceptions.RequestException as e:
            print(f'Error al conectar al servidor: {e}')
        except Exception as e:
            print(f'Error inesperado al conectar al servidor: {e}')

    def analizar_enlaces(self, url):
        """
        Inicia el análisis de enlaces en la URL base.

        Args:
            url (str): La URL base a analizar.
        """
        print(f'Analizando enlaces de: {url}')
        self.extraer_y_analizar(url)

if __name__ == "__main__":
    url_base = 'https://www.trip.com'  # Reemplaza con la URL que deseas analizar
    analizador = AnalizadorInyeccionSQL(url_base, profundidad_maxima=3, hilos_maximos=5)
    print("Presiona 'x' en cualquier momento para detener la ejecución.")
    analizador.analizar_enlaces(url_base)