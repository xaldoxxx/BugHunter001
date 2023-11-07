import requests
from bs4 import BeautifulSoup

def get_page_resources(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verificar si la solicitud fue exitosa
        soup = BeautifulSoup(response.text, "html.parser")

        # Obtener todos los recursos cargados (imágenes, hojas de estilo, scripts, etc.)
        resources = []

        # Recopilar imágenes
        img_tags = soup.find_all("img")
        for img in img_tags:
            src = img.get("src")
            if src:
                resources.append(src)

        # Recopilar hojas de estilo
        link_tags = soup.find_all("link", rel="stylesheet")
        for link in link_tags:
            href = link.get("href")
            if href:
                resources.append(href)

        # Recopilar scripts
        script_tags = soup.find_all("script")
        for script in script_tags:
            src = script.get("src")
            if src:
                resources.append(src)

        # Otros recursos pueden ser analizados de manera similar (fuentes, videos, etc.)

        return resources

    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL: {e}")
        return []

if __name__ == "__main__":
    url = "https://portal.au.frontegg.com/"  # Reemplaza con la URL que deseas analizar
    resources = get_page_resources(url)

    if resources:
        print("Recursos cargados en la página:")
        for resource in resources:
            print(resource)
    else:
        print("No se encontraron recursos en la página.")