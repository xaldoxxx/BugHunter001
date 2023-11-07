import http.client

class HttpRequest:
    def __init__(self, url):
        self.url = url

    def send_get_request(self, path="/"):
        conn = http.client.HTTPSConnection(self.url)
        conn.request("GET", path)
        response = conn.getresponse()
        return response

class HttpResponse:
    def __init__(self, response):
        self.status = response.status
        self.headers = response.getheaders()
        self.content = response.read().decode("utf-8")

    def display_status(self):
        print(f'Código de estado HTTP: {self.status}')

    def display_headers(self):
        print('Cabeceras:')
        for key, value in self.headers:
            print(f'{key}: {value}')

    def display_content(self):
        print('\nContenido de la respuesta:')
        print(self.content)

def main():
    url = 'trip.com'

    request = HttpRequest(url)
    response = request.send_get_request()

    http_response = HttpResponse(response)

    http_response.display_status()
    http_response.display_headers()
    http_response.display_content()

if __name__ == "__main__":
    main()