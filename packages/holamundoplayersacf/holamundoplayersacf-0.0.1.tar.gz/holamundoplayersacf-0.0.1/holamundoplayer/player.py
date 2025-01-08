"""
Este es el módulo que incluye la clase de reproductor de música
"""


class Player:
    """
    Esta clase crea un reproductor de música
    """

    def play(self, song):
        """
        Reproduce la canción que recibió como parámetro

        Parameters:
        song (str): este es un string con el path de la canción

        Returns:
        int: devuelve 1 si reproduce con éxito, de lo contrario devuelve 0
        """
        print("Reproduciendo canción...")

    def stop(self):
        print("Stopping...")
