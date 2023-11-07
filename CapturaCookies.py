import http.client
import http.cookies
import urllib.parse
import pickle

class CookieCapture:
    def __init__(self, url, user_agent=None):
        self.url = url
        self.user_agent = user_agent
        self.cookies = None

    def capture_cookies(self):
        try:
            # Parsea la URL
            url_parts = urllib.parse.urlparse(self.url)
            conn = http.client.HTTPSConnection(url_parts.netloc)

            # Configura el encabezado User-Agent si se proporciona
            headers = {}
            if self.user_agent:
                headers["User-Agent"] = self.user_agent

            # Realiza la solicitud GET
            conn.request("GET", url_parts.path, headers=headers)
            response = conn.getresponse()

            # Obtiene las cabeceras HTTP de la respuesta
            headers = response.getheaders()

            # Inicializa un objeto SimpleCookie para analizar las cookies
            cookie_parser = http.cookies.SimpleCookie()

            # Busca las cabeceras "Set-Cookie" en la respuesta
            for header in headers:
                if header[0].lower() == "set-cookie":
                    cookie_parser.load(header[1])

            # Almacena las cookies en un diccionario
            self.cookies = {name: cookie.value for name, cookie in cookie_parser.items()}

            return True

        except Exception as e:
            print(f"Error al capturar cookies: {str(e)}")
            return False

    def get_cookies(self):
        return self.cookies

    def save_cookies(self, filename):
        try:
            with open(filename, "wb") as file:
                pickle.dump(self.cookies, file)
            print(f"Cookies guardadas en '{filename}'")
            return True
        except Exception as e:
            print(f"Error al guardar las cookies: {str(e)}")
            return False

    def load_cookies(self, filename):
        try:
            with open(filename, "rb") as file:
                self.cookies = pickle.load(file)
            print(f"Cookies cargadas desde '{filename}':")
            return True
        except Exception as e:
            print(f"Error al cargar las cookies: {str(e)}")
            return False

    def print_cookies(self):
        if self.cookies:
            print("Cookies capturadas:")
            for name, value in self.cookies.items():
                print(f"Nombre: {name}")
                print(f"Valor: {value}")
            print("-" * 40)
        else:
            print("No se han capturado cookies.")

if __name__ == "__main__":
    # Define la URL de inicio de sesión
    login_url = "https://www.trip.com/"

    # Define el User-Agent para simular diferentes navegadores (opcional)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    # Crea una instancia de CookieCapture y captura las cookies
    cookie_capturer = CookieCapture(login_url, user_agent=user_agent)
    if cookie_capturer.capture_cookies():
        cookies = cookie_capturer.get_cookies()
        print("Cookies capturadas con éxito:")
        cookie_capturer.print_cookies()

        # Guarda las cookies en un archivo (opcional)
        if cookie_capturer.save_cookies("captured_cookies.pkl"):
            # Carga las cookies desde el archivo (opcional)
            if cookie_capturer.load_cookies("captured_cookies.pkl"):
                print("Cookies cargadas desde 'captured_cookies.pkl':")
                cookie_capturer.print_cookies()
    else:
        print("No se pudieron capturar las cookies.")