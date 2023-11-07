import requests
import socket
import http.cookies
import platform

class WebInfoCollector:
    def __init__(self, url):
        self.url = url
        self.response = None
        self.cookies = None
        self.ip_addresses = None
        self.user_agent = None

    def fetch_url(self):
        try:
            self.response = requests.get(self.url)
            self.cookies = http.cookies.SimpleCookie()
            self.cookies.load(self.response.headers.get('Set-Cookie', ''))
            self.ip_addresses = socket.gethostbyname_ex(socket.gethostname())
            self.user_agent = self.get_user_agent()
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud a {self.url}: {e}")

    def get_user_agent(self):
        return f"Python ({platform.system()}; {platform.machine()})"

    def display_info(self):
        print(f"URL: {self.url}")
        print(f"Status Code: {self.response.status_code}")
        print("Cookies:")
        for cookie in self.cookies:
            print(f"{cookie}: {self.cookies[cookie].value}")
        print("IP Addresses:")
        for ip_address in self.ip_addresses[2]:
            print(ip_address)
        print(f"User Agent: {self.user_agent}")
        print("Response Content:")
        print(self.response.text)

    def save_response_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.response.text)

if __name__ == "__main__":
    url = "https://trip.com/"  # Reemplaza con la URL que deseas analizar
    collector = WebInfoCollector(url)
    collector.fetch_url()
    collector.display_info()
    collector.save_response_to_file("response.txt")