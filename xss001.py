# xss
import requests
from bs4 import BeautifulSoup

class XSSScanner:
    def __init__(self, base_url):
        self.base_url = base_url

    def scan_xss_vulnerabilities(self):
        try:
            # Realiza una solicitud GET al URL base.
            response = requests.get(self.base_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Busca todos los campos de entrada en formularios HTML.
                forms = soup.find_all('form')
                for form in forms:
                    inputs = form.find_all('input')
                    for input_field in inputs:
                        # Verifica si el campo de entrada es vulnerable a XSS almacenado o reflejado.
                        input_name = input_field.get('name')
                        if input_name:
                            self.test_xss(input_name)

        except requests.RequestException as e:
            print(f'Error al conectar al servidor: {e}')

    def test_xss(self, input_name):
        # Envía una solicitud POST con un payload XSS de prueba para verificar si el campo es vulnerable.
        payload = f"<script>alert('XSS')</script>"
        data = {input_name: payload}
        response = requests.post(self.base_url, data=data)

        if payload in response.text:
            print(f'Vulnerabilidad de XSS detectada en el campo: {input_name}')

if __name__ == "__main__":
    url = 'https://www.xaldoxxx.com.ar/'  # Reemplaza con la URL que deseas analizar
    scanner = XSSScanner(url)
    scanner.scan_xss_vulnerabilities()
