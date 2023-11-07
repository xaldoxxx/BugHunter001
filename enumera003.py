# recupera enlaces y subenlaces
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class HTMLLinkExtractor:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()

    def extract_links(self, url, depth=0):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = [a.get('href') for a in soup.find_all('a')]

                self.visited_urls.add(url)

                if depth > 0:
                    print(f"Recopilando enlaces de {url}:")
                    for link in links:
                        full_url = urljoin(url, link)
                        parsed_url = urlparse(full_url)

                        # Filtrar enlaces internos y evitar duplicados.
                        if parsed_url.netloc == urlparse(self.base_url).netloc and full_url not in self.visited_urls:
                            print(full_url)
                            self.extract_links(full_url, depth - 1)
        except requests.RequestException as e:
            print(f'Error al conectar al servidor: {e}')
        except Exception as e:
            print(f'Error inesperado: {e}')

if __name__ == "__main__":
    base_url = 'https://www.trip.com/'  # Reemplaza con la URL que deseas analizar
    link_extractor = HTMLLinkExtractor(base_url)
    link_extractor.extract_links(base_url, depth=3)  # Cambia la profundidad según tus necesidades