# chromolog [Versión actual: 0.2.0](https://pypi.org/project/chromolog/)

Imprima mensajes por consola coloridos y distinguidos de los demás, tenga un formato de salida por consola más elegante y vívido según lo prefiera, ya sea un mensaje de `error` o un mensaje de operación finalizada (`success`).

# Inicialización

1. Importación del módulo
2.  Crear una instancia de la clase `Print` 
3.  Use los [métodos disponibles](#métodos-disponibles).

# Métodos Disponibles
- `err(err:any)`: Indicado para imprimir los errores 😞
- `inf(inf:any)`: Indicado para imprimir mensajes de precacución, variables ℹ
- `warn(warn:any)`: Indicado para imprimir mensajes de precacución 😱
- `suc(suc:any)`: Indicado para indicar que la ejecución fue completada con éxito ✅

Visite: https://tutosrivegamerlq.github.io/chromolog/ para más detalles


## Historial de versiones:
- `v0.2.0`: 
  - Mejoras del proyecto, ahora solo debe importar: `import chromolog`.
  - Nuevos métodos:
    - `exc(exc:Exception)`: Específico para imprimir la información precisa de una excepción capturada con el bloque `try`
- `v0.1.1`: Corrección de errores de la página del proyecto en https://pypi.org
- `v0.1.0`: Primera versión funcional.

Si desea conocer más acerca de, visite:
- [Web de soporte](https://tutosrivegamerlq.github.io/chromolog/)
- [Web pypi.org](https://pypi.org/project/chromolog/)
- [Github project](https://github.com/tutosrivegamerLQ/chromolog/)