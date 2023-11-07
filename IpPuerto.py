import socket

def obtener_info_url(url):
    try:
        host = url.split('//')[1].split('/')[0]
        ip = socket.gethostbyname(host)
        port = 80  # Puerto predeterminado para HTTP

        return ip, port
    except Exception as e:
        return None, None

# URL de ejemplo
url = "https://www.trip.com/"

ip, port = obtener_info_url(url)

if ip and port:
    print(f'IP: {ip}')
    print(f'Puerto: {port}')
else:
    print("No se pudo obtener la información de la URL.")