"""
Este es el modulo que incluye la clase de reproductor de musica
"""


class Player:
    """
    Esta clase crea un reproductor
    de musica
    """

    def play(self, song):
        """
        Reproduce la cancion que recibio en el constructor

        Parameters:
        song (str): Este es un string con el path de la cancion

        Returns:
        int: devuelve 1 si reproduce con exito, en caso de fracaso devuelve cero
        """
        print("reproduciendo candion")

    def stop(self):
        print("stoping")

# pip3 install setuptools wheel twine # nos permite generar los empaquetados y subirlos a pypi
# python3 setup.py sdist bdist_wheel # para publicar nuestro paquete sdist=source distribution; bdist=build distribution
