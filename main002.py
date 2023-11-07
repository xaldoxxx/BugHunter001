import subprocess
import requests
import os


class AnalisisWeb:
    def __init__(self, objetivo):
        self.objetivo = objetivo

    def analizar_xss(self):
        try:
            resultado = subprocess.check_output(['xsser', '-u', self.objetivo], text=True)
            return resultado
        except Exception as e:
            return str(e)

    def analizar_sql_injection(self):
        try:
            resultado = subprocess.check_output(['sqlmap', '-u', self.objetivo], text=True)
            return resultado
        except Exception as e:
            return str(e)

    def analizar_encabezados(self):
        try:
            response = requests.head(self.objetivo)
            encabezados = response.headers
            return encabezados
        except Exception as e:
            return str(e)

    def escanear_vulnerabilidades_comunes(self):
        try:
            resultado = subprocess.check_output(['nikto', '-h', self.objetivo], text=True)
            return resultado
        except Exception as e:
            return str(e)

    def crear_carpeta_de_resultados(self):
        if not os.path.exists('resultados'):
            os.makedirs('resultados')

    def guardar_resultados(self, nombre_archivo, resultado):
        with open(os.path.join('resultados', nombre_archivo), 'w') as archivo:
            archivo.write(resultado)


if __name__ == '__main__':
    url_objetivo = 'https://jobs.porsche.com/index.php?ac=start'



    analisis = AnalisisWeb(url_objetivo)

    analisis.crear_carpeta_de_resultados()

    resultado_xss = analisis.analizar_xss()
    analisis.guardar_resultados('resultado_xss.txt', resultado_xss)
    print("Resultados de XSS:")
    print(resultado_xss)

    resultado_sql_injection = analisis.analizar_sql_injection()
    analisis.guardar_resultados('resultado_sql_injection.txt', resultado_sql_injection)
    print("\nResultados de SQL Injection:")
    print(resultado_sql_injection)

    encabezados = analisis.analizar_encabezados()
    analisis.guardar_resultados('encabezados_http.txt', str(encabezados))
    print("\nEncabezados HTTP:")
    print(encabezados)

    resultado_vulnerabilidades = analisis.escanear_vulnerabilidades_comunes()
    analisis.guardar_resultados('resultado_vulnerabilidades.txt', resultado_vulnerabilidades)
    print("\nResultados de Escaneo de Vulnerabilidades Comunes:")
    print(resultado_vulnerabilidades)
sqlmap -u <target URL> — dbs