'''
analizador de inyección SQL que se utiliza para escanear un sitio web en busca
de formularios y enlaces. Su objetivo es identificar formularios en páginas web
y analizar su estructura, como la acción del formulario, el método de envío y
los campos de entrada. Además, el analizador también sigue los enlaces dentro
del sitio web y realiza un análisis similar en esas páginas.
'''

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
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'X-Hackerone': 'eltontito'
            }

            max_retries = requests.packages.urllib3.util.retry.Retry(
                total=5,
                status_forcelist=[429, 500, 502, 503, 504]
            )
            adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
            session = requests.Session()
            session.mount("https://", adapter)

            if not url.startswith('http'):
                url = urljoin(self.url_base, url)

            if not url.startswith(self.url_base):
                return  # No analizar URL externas

            response = session.get(url, headers=headers, verify=True)

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
                        futuros = {executor.submit(self.extraer_y_analizar, enlace.get('href'), profundidad + 1): enlace for enlace in soup.find_all('a') if enlace.get('href')}
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
    url_base = 'https://ahoracalafate.com.ar/a_default/user/login'  # Reemplaza con la URL que deseas analizar
    analizador = AnalizadorInyeccionSQL(url_base, profundidad_maxima=3, hilos_maximos=5)
    print("Presiona 'x' en cualquier momento para detener la ejecución.")
    analizador.analizar_enlaces(url_base)
