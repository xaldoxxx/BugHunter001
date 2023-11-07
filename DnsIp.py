import socket
import requests
import ssl

def obtener_info_url(url):
    try:
        host = url.split('//')[1].split('/')[0]
        ip = socket.gethostbyname(host)
        port = 80  # Puerto predeterminado para HTTP
        dns_info = socket.gethostbyaddr(ip)

        # Obtener información de organización y país utilizando una solicitud HTTP
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            info = response.json()
            organizacion = info.get("org", "Desconocido")
            pais = info.get("country", "Desconocido")
        else:
            organizacion = "Desconocido"
            pais = "Desconocido"

        # Verificar si el sitio web utiliza HTTPS y si el certificado SSL es válido
        ssl_info = ssl.create_default_context().wrap_socket(socket.socket(), server_hostname=host)
        cert = ssl_info.getpeercert()
        https_usado = "Sí" if ssl_info.version() == ssl.PROTOCOL_TLS and cert else "No"

        # Aquí puedes agregar verificaciones de registros DNS adicionales, como SPF, DKIM, DMARC, si es necesario

        return ip, port, dns_info, organizacion, pais, https_usado
    except Exception as e:
        return None, None, None, None, None, "Desconocido"

# URL de ejemplo
url = "https://www.trip.com//"

ip, port, dns_info, organizacion, pais, https_usado = obtener_info_url(url)

if ip and port:
    print(f'IP: {ip}')
    print(f'Puerto: {port}')
    print(f'DNS Info: {dns_info}')
    print(f'Organización: {organizacion}')
    print(f'País: {pais}')
    print(f'¿HTTPS Usado?: {https_usado}')
else:
    print("No se pudo obtener la información de la URL.")