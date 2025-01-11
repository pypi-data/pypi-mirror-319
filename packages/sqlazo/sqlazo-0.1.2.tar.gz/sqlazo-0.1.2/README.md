# SQLAZO

Es un módulo para gestionar bases de datos _SQLITE_. Le permite acceder a métodos que realizan **transacciones** con la base de datos que usted elija, siempre y cuando sea una base de datos _SQLITE_

## Inicialización

Para iniciar, su uso, se hará una instancia de la clase **Database**, la cual recibe los siguientes parámetros:

`name:str`: Nombre de la base de datos (Ej: `'test.db'`).
`check_thread:boolean`: Verificar ejecuciones multihilo.

```py
# Ejemplo de inicialización
from sqlazo import Database

db = Database('test.db', False)
# Creará un archivo test.db listo para usar...
```

## Métodos disponibles

- `create_table`: Permite crear una tabla en la base de datos conectada.
- `insert_data`: Ejecuta la "consulta" de inserción en la base de datos (Agrega datos).
- `get_data_all`: Ejecuta la "consulta" para obtener todos los registros de la base de datos.
- `get_data_where`: Ejecuta la "consulta" para obtener registros con "consulta personalizada".
- `delete_data`: Eliminar registros dea base de datos.

## Métodos privados 🔏
- `__connect`: Realizar conexión a la base de datos.
- `__commit`: "Refrescar" cambios en la base de datos.
- `__cursor`: Crea un cursor en la conexión a la base de datos, el cual permite "ejecutar consultas".

## Historial de versiones:
- `0.1.2`: Actualización de versiones de dependencias
- `0.1.1`: Se agregó el manejo de dependencias en el archivo de construcción (.toml)
- `0.1.0`: Versión inicial

## Si desea conocer más acerca de, visite:
- [Web de soporte](https://tutosrivegamerlq.github.io/sqlazo/)
- [Web pypi.org](https://pypi.org/project/sqlazo/)
- [Github project](https://github.com/tutosrivegamerLQ/sqlazo/)