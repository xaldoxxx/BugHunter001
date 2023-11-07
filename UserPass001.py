# busca nombre de usuario y contraseña
import requests
from bs4 import BeautifulSoup

class WeakCredentialsScanner:
    def __init__(self, base_url):
        self.base_url = base_url

    def scan_weak_credentials(self):
        try:
            response = requests.get(self.base_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Busca formularios de inicio de sesión en la página.
                login_forms = soup.find_all('form', {'method': 'post'})

                for form in login_forms:
                    username_field = self.find_username_field(form)
                    password_field = self.find_password_field(form)

                    if username_field and password_field:
                        self.check_weak_credentials(username_field, password_field)

        except requests.RequestException as e:
            print(f'Error al conectar al servidor: {e}')

    def find_username_field(self, form):
        # Busca un campo de entrada que se parezca a un nombre de usuario.
        username_field = form.find('input', {'type': 'text', 'name': re.compile(r'user|username|email')})
        return username_field

    def find_password_field(self, form):
        # Busca un campo de entrada que se parezca a una contraseña.
        password_field = form.find('input', {'type': 'password', 'name': re.compile(r'pass|password')})

        return password_field    def check_weak_credentials(self, username_field, password_field):
        # Aquí puedes agregar lógica para verificar si los valores predeterminados son débiles.
        # Por ejemplo, comparar con una lista de nombres de usuario y contraseñas débiles.

        # Ejemplo simple: Verificar si el campo de contraseña tiene un valor predeterminado "password".
    if password_field.get('value') == 'password':
            print(f'Contraseña débil encontrada en el formulario de inicio de sesión.')

if __name__ == "__main__":
    url = 'https://www.xaldoxxx.com.ar/'  # Reemplaza con la URL que deseas analizar
    scanner = WeakCredentialsScanner(url)
    scanner.scan_weak_credentials()
