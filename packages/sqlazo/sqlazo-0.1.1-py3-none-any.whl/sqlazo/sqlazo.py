"""Sqlazo para gestionar bases de datos SQLITE

Le permite acceder a métodos que realizan transacciones con la base de datos que usted elija,
siempre y cuando sea una base de datos SQLITE

@author Tutos Rive Gamer

Historial de versiones:
- `0.1.1`: Se agregó el manejo de dependencias en el archivo de construcción (.toml)
- 0.1.0: Versión inicial
"""

import sqlite3 as sql
from chromologger import Logger

__version__ = "0.1.1"
__author__ = "Tutos Rive Gamer"

# Escritor de registros
log = Logger()

class Database:
	""" Manipular base de datos """
	def __init__(self, name, check_thread) -> None:
		# Nombre base de datos
		self.name:str = name
		# Verificar "Multi Hilo"
		self.check:bool = check_thread
		# Conexión
		self.conn:sql.Connection = self.__connect()
		# Cursor
		self.cur:sql.Cursor = self.__cursor()

	def __connect(self) -> sql.Connection | int:
		"""Crear conexión con la base de datos
		
		Returns:
			`sql.Connection | int`: 
				`sql.Cursor`: Si no hay errores
				`int`: `-1`, ocurrió un error
		"""
		try:
			return sql.connect(self.name, check_same_thread=self.check)
		except sql.Error as e:
			log.log_e(e)
			return -1

	def __cursor(self) -> sql.Cursor | int:
		"""Agregar un cursor a la conexión

		Returns:
			`sql.Cursor | int`: 
				`sql.Cursor`: Si no hay errores
				`int`: `-1`, ocurrió un error
		"""
		try:
			return self.conn.cursor()
		except sql.Error as e:
			log.log_e(e)
			return -1
	    
	def create_table(self, table_name:str, cols:list) -> bool:
		"""Crear tabla en base de datos

		Args:
			`table_name:str`: Nombre de la tabla que se quiere crear
			`cols:list`: Columnas que se agregarán a la tabla

		Returns:
			`bool`: 
				`False`: Operación con errores
				`True`: Operación sin errores
		"""
		# Informar al usuario donde está el error que verá en la base de datos...
		tp:type = type(cols)
		if tp == list:
			# Separar columnas por coma
			try:
				cols:str = ', '.join(cols)
				self.cur.execute(f'CREATE TABLE {table_name} ({cols})')
				# Operación ejecutada, retornar nombre de tabla creada
				return True
			except sql.Error as error:
				# print(error)
				log.log_e(error)
				# Hubieron errores
				return False
		else:
			log.log(f'Se recibió {tp} como atributo cols, debería ser de tipo {type([])}')
			# Hubieron errores
			return False
	
	def insert_data(self, data:list, cols:list, table_name:str) -> bool:
		"""Inserta datos en una tabla específica.

			Args:
			    `data:list`: Lista de valores a insertar
			    `cols:list`: Columnas correspondientes a los valores
			    `table_name:str`: Nombre de la tabla donde se insertarán los datos

			Returns:
			    `bool`: `True` si la inserción fue exitosa, `False` en caso de error
			"""
		try:
			# Signos '?'' para evitar sqlInjection
			sign:str = ', '.join(['?' for _ in cols])
			try:
	        	# Formato consulta SQL
				query:str = f'INSERT INTO {table_name} ({", ".join(cols)}) VALUES ({sign})'
	        	# Ejecución de la consulta SQL
				self.cur.execute(query, data)
	        	# Actualizar cambios
				self.__commit()
				return True
			except sql.Error as error:
				log.log_e(error)
				return False
		except TypeError as e:
			log.log_e(e)
			return False
	        
	def get_data_all(self, tablename:str) -> sql.Cursor | None:
		"""Obtener toda la información de una tabla

		Args:
			`tablename:str`: Nombre de la tabla

		Returns:
			`sql.Cursor` | `None`: `sql.Cursor` si la ejecución fue exitosa, `None` en caso de error
		"""
		try:
			return self.cur.execute(f'SELECT * FROM {tablename}')
		except sql.Error as e:
			log.log_e(e)
	
	def get_data_where(self, table_name:str, condition:str, *args:str) -> sql.Cursor | None:
		"""Seleccionar datos con una condición

		Args:
			`table_name:str`: 
			`condition:str`: 

		Returns:
			sql.Cursor | None: _description_
		"""
		args = ", ".join(args) if len(args) > 0 else '*'
		try:
			return self.cur.execute(f'SELECT {args} FROM {table_name} WHERE {condition}')
		except sql.Error as error:
			log.log_e(error)
	    
	def delete_data(self, table:str, condition:str) -> bool:
		"""Eliminar elementos de la base de datos

		Args:
			`table:str`: Nombre de la tabla
			`condition:str`: Condición que debe cumplir el elemento para poderse eliminar (`WHERE`)

		Returns:
			`bool`: `True` si la operación fue exitosa, `False` en caso de error
		"""
		if len(condition.replace(' ', '')) > 2:	
			try:
				query = self.cur.execute(f'DELETE FROM {table} WHERE {condition}')
				self.__commit()
				return True
			except sql.Error as error:
				log.log_e(error)
				return False
		else:
			log.log('No se especificó una condición (WHERE) válida al momento de eliminar un dato')
	
	def __commit(self) -> bool:
		""" Actualizar cambios 

			Returns:
				`bool`: `True` si el cambio fue exitoso, `False` en caso de rror
		"""
		try:
			self.conn.commit()
			return True
		except sql.Error as e:
			log.log_e(e)
			return False
	
	def close(self) -> bool:
		"""Cerrar conexión con la base de datos

		Returns:
			`bool`: `True` si la base de la conexión fue cerrada con éxito, `False` en caso de error
		"""
		try:
			self.conn.close()
			return True
		except sql.Error as e:
			log.log_e(e)
			return False