# puertos abiertos y ftp

import socket
import ftplib
import urllib.parse

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

    def check_open_ports(self, target_host, ports):
        open_ports = []
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_host, port))
            sock.close()
            if result == 0:
                open_ports.append(port)
        return open_ports

if __name__ == "__main__":
    url = 'ftp://ftp.xaldoxxx.com.ar/'  # Reemplaza con la URL que deseas analizar
    analyzer = URLAnalyzer(url)

    # Comprueba la conexión FTP
    ftp_connection = analyzer.check_ftp_connection()
    if ftp_connection:
        print("Conexión FTP exitosa.")
    else:
        print("Error en la conexión FTP o la URL no es compatible con FTP.")

    # Comprueba puertos abiertos
    target_host = urllib.parse.urlparse(url).hostname
    ports_to_check = [21, 80, 443]  # Puertos que deseas verificar
    open_ports = analyzer.check_open_ports(target_host, ports_to_check)
    if open_ports:
        print("Puertos abiertos encontrados:", open_ports)
    else:
        print("No se encontraron puertos abiertos.")