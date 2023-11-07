# https://www.yelp.com/login?return_url=https%3A%2F%2Fwww.yelp.com%2Fsearch%3Ffind_desc%3D%253C%2Blisting%2Bid%253Dx%253E%2526lt%253Bimg%2Bsrc%253D1%2Bonerror%253Dalert(1)%2526gt%253B%253C%2B%252Flisting%253E%2B%253C%2Bscript%253Ealert(document.getElementById(%2527x%2527).innerHTML)%253C%2B%252Fscript%253E%26find_loc%3DCaballito%252C%2BBuenos%2BAires%252C%2BArgentina
import http.client
import http.cookies
import urllib.parse
import pickle
import requests
from datetime import datetime

class CookieCapture:
    def __init__(self, url, user_agent=None):
        self.url = url
        self.user_agent = user_agent
        self.cookies = None

    def capture_cookies(self):
        try:
            url_parts = urllib.parse.urlparse(self.url)
            conn = http.client.HTTPSConnection(url_parts.netloc)
            headers = {"User-Agent": self.user_agent} if self.user_agent else {}

            conn.request("GET", url_parts.path, headers=headers)
            response = conn.getresponse()
            headers = response.getheaders()

            cookie_parser = http.cookies.SimpleCookie()
            for header in headers:
                if header[0].lower() == "set-cookie":
                    cookie_parser.load(header[1])

            self.cookies = {key: cookie.value for key, cookie in cookie_parser.items()}
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
            return True
        except Exception as e:
            print(f"Error al guardar las cookies: {str(e)}")
            return False

    def load_cookies(self, filename):
        try:
            with open(filename, "rb") as file:
                self.cookies = pickle.load(file)
            return True
        except Exception as e:
            print(f"Error al cargar las cookies: {str(e)}")
            return False

    def print_cookies(self):
        if self.cookies:
            print("Cookies capturadas:")
            for name, cookie in self.cookies.items():
                print(f"Nombre: {name}")
                print(f"Valor: {cookie}")
                if "domain" in cookie:
                    print(f"Dominio: {cookie['domain']}")
                if "secure" in cookie:
                    print("Secure: Sí")
                if "httponly" in cookie:
                    print("HttpOnly: Sí")
                if "expires" in cookie:
                    print(f"Expiración: {cookie['expires']}")
                print("-" * 40)
        else:
            print("No se han capturado cookies.")

    def verify_security_attributes(self):
        secure_cookies = [name for name, cookie in self.cookies.items() if "secure" not in cookie]
        httponly_cookies = [name for name, cookie in self.cookies.items() if "httponly" not in cookie]

        print("Cookies no Secure:", secure_cookies)
        print("Cookies no HttpOnly:", httponly_cookies)

    def check_cookie_expiration(self):
        current_time = datetime.now()
        for name, cookie in self.cookies.items():
            if "expires" in cookie:
                expiration_date = cookie["expires"]
                try:
                    expiration_datetime = datetime.strptime(expiration_date, "%a, %d-%b-%Y %H:%M:%S GMT")
                    if expiration_datetime > current_time:
                        print(f"Cookie {name} con fecha de expiración en el futuro: {expiration_date}")
                    else:
                        print(f"Cookie {name} caducada: {expiration_date}")
                except ValueError:
                    print(f"Formato de fecha de expiración no válido para la cookie {name}: {expiration_date}")
            else:
                print(f"Cookie {name} sin fecha de expiración")

    def block_cookies(self, cookies_to_block):
        for cookie_name in cookies_to_block:
            if cookie_name in self.cookies:
                del self.cookies[cookie_name]

    def identify_tracking_cookies(self):
        tracking_cookies = [
            {
                "Nombre": name,
                "Valor": cookie.value,
                "Dominio": cookie["domain"] if "domain" in cookie else "",
                "Secure": "Secure" if "secure" in cookie else "",
                "HttpOnly": "HttpOnly" if "httponly" in cookie else "",
                "Expiración": cookie["expires"] if "expires" in cookie else "",
            }
            for name, cookie in self.cookies.items() if isinstance(cookie, http.cookies.Morsel)
        ]

        print("Cookies de seguimiento:")
        for cookie_info in tracking_cookies:
            for key, value in cookie_info.items():
                print(f"{key}: {value}")
            print("-" * 40)

    def identify_session_cookies(self):
        session_cookies = [name for name, cookie in self.cookies.items() if "expires" not in cookie]

        print("Cookies de sesión:")
        for cookie_name in session_cookies:
            print("Nombre:", cookie_name)
        print("-" * 40)

    def show_privacy_policies(self):
        pass

    def show_cookie_stats(self):
        print("Número total de cookies:", len(self.cookies))

if __name__ == "__main__":
    login_url = "https://www.visa.com.mx/search.html?q=" + "1 and 1=1– –"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    cookie_capturer = CookieCapture(login_url, user_agent=user_agent)
    if cookie_capturer.capture_cookies():
        cookies = cookie_capturer.get_cookies()
        print("Cookies capturadas con éxito:")
        cookie_capturer.print_cookies()

        cookie_capturer.verify_security_attributes()
        cookie_capturer.check_cookie_expiration()
        cookie_capturer.identify_tracking_cookies()
        cookie_capturer.identify_session_cookies()
        cookie_capturer.show_cookie_stats()

    else:
        print("No se pudieron capturar las cookies.")