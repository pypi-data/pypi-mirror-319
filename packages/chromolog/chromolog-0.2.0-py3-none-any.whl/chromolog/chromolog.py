
# v0.2.0
"""Micromódulo para imprimir mensajes en consola con texto de colores.

Este módulo permite personalizar mensajes dinámicos en consola, incluyendo
texto en diferentes colores.


Historial de versiones:
- `v0.2.0`: Mejoras del proyecto, ahora solo debe importar: `import chromolog`.
- `v0.1.1`: Corrección de errores de la página del proyecto en https://pypi.org
- `v0.1.0`: Primera versión funcional.

Revise el historial completo aquí: [Historial completo de veriones](https://github.com/tutosrivegamerLQ/chromolog/#historial-de-versiones)

@author Tutos Rive Gamer

Si desea conocer más acerca de, visite:
- [Web de soporte](https://tutosrivegamerlq.github.io/chromolog/)
- [Web pypi.org](https://pypi.org/project/chromolog/)
- [Github project](https://github.com/tutosrivegamerLQ/chromolog/)
"""

import traceback

__version__ = "0.1.1"
__author__ = "Tutos Rive Gamer"


class Print:
    """Imprimir mensajes por consola con color de texto (`error`, `warning`, `succes`, `info`)
    """
    def __init__(self) -> None:
        self.RES = '\u001B[0m' # Resetear color
        self.RED = '\u001B[31m'
        self.YELLOW = '\u001B[33m'
        self.BLUE = '\u001B[34m'
        self.GREEN = '\u001B[32m'
    
    def __str__(self):
        return f'Módulo: chromolog\nClase principal: Print\nVerisón: {__version__}\nAutor: {__author__}'

    def err(self, err:any) -> None:
        """Imprimir errores (Color Texto: Rojo)

        Args:
            `err:any`: Error que se imprimirá
        """
        self.__w(f'{self.RED}{err}{self.RES}')
    
    def exc(self, exc: Exception) -> None:
        """Imprimir errores de Excepciones específicas (Color Texto: Rojo)

        Args:
            `exc:Exception`: Excepción capturada con bloque try
        """
        trace:dict = self.__traceback(exc)
        self.err(f'Exception: {exc.__class__.__name__}\nFile: {trace.get('path')}\nErrorLine: {trace.get('line')}\nMesssage: {exc}')


    def inf(self, inf:any) -> None:
        """Imprimir información (Color Texto: Azul)

        Args:
            `inf:any`: Información que se imprimirá
        """
        self.__w(f'{self.BLUE}{inf}{self.RES}')

    def warn(self, warn:any) -> None:
        """Imprimir mensajes de precaución (Color Texto: Amarillo)

        Args:
            `warn:any`: Mensaje que se imprimirá
        """
        self.__w(f'{self.YELLOW}{warn}{self.RES}')

    def suc(self, suc:any) -> None:
        """Imprimir mensajes de éxito (Final de ejecución, podría ser...) (Color Texto: Verde)

        Args:
            `suc:any`: Mensaje que se imprimirá
        """
        self.__w(f'{self.GREEN}{suc}{self.RES}')

    def __w(self, msg:any) -> None:
        """Imprimir mensaje con colores

        Args:
            `msg:any`: Mensaje que se imprimirá
        """
        print(msg)
    
    def __traceback(self, e:Exception) -> dict:
        """Obtener un registro preciso de la excepción

        Args:
            `e:Exception`: Excepción con la cual se trabajará

        Returns:
            `dict`: Diccionario con claves: {`line`: (Línea del error),`path`: (Ruta del archivo de error)}
        """
        trace_back = traceback.extract_tb(e.__traceback__)
        return {'line': trace_back[-1][1], 'path': trace_back[-1][0]}

    def test(self) -> None:
        """Ejecutar prueba
        """
        try:
            a = ''
            a += 12
        except TypeError as e:
            self.err(f'err(err) -> Error: {e.__class__.__name__}, Mensaje: {e.__str__()}')
        self.inf('inf(inf) -> Hello World')
        self.warn('warn(warn) -> Precaución, tenga cuidado')
        self.suc('suc(suc) -> Ejecución finalizada...')

if __name__ == '__main__':
    p = Print()
    p.test()