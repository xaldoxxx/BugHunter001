# puertos abiertos y ftp
import ftplib
import socket
import urllib.request

class URLAnalyzer:
    def __init__(self, url):
        self.url = url

    def check_ftp_connection(self):
        try:
            parsed_url = urllib.parse.urlparse(self.url)
            if parsed_url.scheme == 'ftp':
                ftp = ftplib.FTP(parsed_url.hostname)
                ftp.login()
                ftp.quit()
                return True
            return False
        except (ftplib.error_perm, socket.gaierror):
            return False

    def check_open_ports(self, ports):
        try:
            parsed_url = urllib.parse.urlparse(self.url)
            target_host = parsed_url.hostname
            open_ports = []

            for port in ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target_host, port))
                sock.close()
                if result == 0:
                    open_ports.append(port)

            return open_ports

        except (socket.gaierror, socket.error):
            return []

    def check_proxy_configuration(self):
        # Realiza una solicitud a una URL que debe pasar a través del proxy y verifica si la respuesta es la esperada.
        proxy_url = 'http://xaldoxxx.com.ar'  # Reemplaza con tu configuración de proxy
        proxy_support = urllib.request.ProxyHandler({'http': proxy_url})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

        try:
            response = urllib.request.urlopen(self.url)
            if response.status == 200:
                return "Configuración de proxy correcta."
            else:
                return "Configuración de proxy incorrecta."

        except urllib.error.URLError as e:
            return f"Error al conectar a través del proxy: {e}"

if __name__ == "__main__":
    url = 'ftp://ftp.dlptest.com/'  # Reemplaza con la URL que deseas analizar
    analyzer = URLAnalyzer(url)

    # Comprueba la conexión FTP
    ftp_connection = analyzer.check_ftp_connection()
    if ftp_connection:
        print("La conexión FTP es exitosa.")
    else:
        print("Error en la conexión FTP o la URL no es compatible con FTP.")

    # Comprueba los puertos abiertos
    ports_to_check = [21, 80, 443]  # Puertos que deseas verificar
    open_ports = analyzer.check_open_ports(ports_to_check)
    if open_ports:
        print("Puertos abiertos encontrados:", open_ports)
    else:
        print("No se encontraron puertos abiertos.")

    # Comprueba la configuración del proxy
    proxy_configuration = analyzer.check_proxy_configuration()
    print(proxy_configuration)
