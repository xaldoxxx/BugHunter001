# analiza si una url es suceptible a inyeccion sql
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class SQLInjectionAnalyzer:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()

    def extract_and_analyze(self, url, depth=0):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                forms = soup.find_all('form')

                self.visited_urls.add(url)

                if forms:
                    print(f"Analizando URL: {url}")

                for form in forms:
                    action = form.get('action')
                    if action:
                        form_url = urljoin(url, action)
                        parsed_url = urlparse(form_url)

                        if parsed_url.netloc == urlparse(self.base_url).netloc:
                            print(f'Formulario encontrado en {url}')
                            print(f'Acción del formulario: {form_url}')
                            print(f'Método del formulario: {form.get("method", "GET")}')
                            print('Campos del formulario:')

                            for input_field in form.find_all('input'):
                                field_name = input_field.get('name')
                                if field_name:
                                    print(f' - {field_name}')

                if depth > 0:
                    for link in soup.find_all('a'):
                        full_url = urljoin(url, link.get('href'))
                        if full_url not in self.visited_urls:
                            self.extract_and_analyze(full_url, depth - 1)

        except requests.RequestException as e:
            print(f'Error al conectar al servidor: {e}')
        except Exception as e:
            print(f'Error inesperado: {e}')

if __name__ == "__main__":
    base_url = 'https://trip.com/carhire/?channelid=14409'  # Reemplaza con la URL que deseas analizar
    analyzer = SQLInjectionAnalyzer(base_url)
    analyzer.extract_and_analyze(base_url, depth=3)  # Cambia la profundidad según tus necesidades
