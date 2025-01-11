import re
import sqlite3

class DB_SQLite():
    def __init__(self, Nombre):
        self.conn = sqlite3.connect(f'{Nombre}.db')
        self.cursor = self.conn.cursor()
    
    def Crear_tabla_nueva(self, Tabla, **columnas):
        columnas = ", ".join(f"{Columna} {Tipo}" for Columna, Tipo in columnas.items())

        Resultado = f'''
            CREATE TABLE IF NOT EXISTS {Tabla} (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                {columnas}
            ) 
        '''

        self.cursor.execute(f'{Resultado}')
        self.conn.commit()

    def Ingresar(self, Tabla, **valores_columnas):
        # Separar las columnas y los valores para la consulta
        columnas = ', '.join(valores_columnas.keys())
        valores = tuple(valores_columnas.values())

        # Crear la consulta de inserción
        placeholders = ', '.join(['?'] * len(valores_columnas))  # Para evitar inyecciones SQL
        consulta = f"INSERT INTO {Tabla} ({columnas}) VALUES ({placeholders})"

        # Ejecutar la consulta
        self.cursor.execute(consulta, valores)
        self.conn.commit()
    
    def Modificar(self, Tabla, Nombre, categoria, nuevo_value):
        if not Tabla.isidentifier():
            raise ValueError(f"El nombre de la tabla '{Tabla}' no es válido.")
        
        if not categoria.isidentifier():
            raise ValueError(f"El nombre de la categoria '{categoria}' no es válido.")
        
        self.cursor.execute(f'''
            UPDATE {Tabla} SET {categoria} = ? WHERE Nombre = ?
        ''', (nuevo_value, Nombre))
        self.conn.commit()

    def Eliminar(self, Tabla, ID):
        if not Tabla.isidentifier():
            raise ValueError(f"El nombre de la tabla '{Tabla}' no es válido.")
        
        self.cursor.execute(f'''
            DELETE FROM {Tabla} WHERE ID = ?
        ''', (ID,))
        self.conn.commit()

    def Consultar(self, Tabla, Agregado=None, Columna='*'):
        # Validar que el nombre de la tabla no sea peligroso
        if not Tabla.isidentifier():
            raise ValueError(f"El nombre de la tabla '{Tabla}' no es válido.")

        # Validar que las columnas sean válidas
        if Columna != '*' and not all(c.strip().isidentifier() for c in Columna.split(',')):
            raise ValueError(f"El nombre de la columna '{Columna}' no es válido.")

        # Construir la consulta base
        consulta = f"SELECT {Columna} FROM {Tabla}"

        # Validar y agregar cláusulas adicionales
        parametros = []
        if not Agregado == None:
            Agregado, parametros = self.validar_agregado(Agregado)
            consulta += f" {Agregado}"

        # Ejecutar la consulta usando parámetros
        self.cursor.execute(consulta, parametros)
        
        return self.cursor.fetchall()

    def validar_agregado(self, agregado):
        # Eliminar espacios extras en toda la cláusula
        agregado = ' '.join(agregado.split())

        # Lista de palabras clave peligrosas
        palabras_clave_peligrosas = ['DROP', 'INSERT']
        for palabra in palabras_clave_peligrosas:
            if palabra in agregado.upper():
                raise ValueError(f"El parámetro {agregado} contiene una cláusula peligrosa: {palabra}")

        # Utilizar expresión regular para capturar condiciones
        partes = re.findall(r"'(.*?)'|\"(.*?)\"|(\S+)", agregado)

        parametros = []  # Lista de valores para los placeholders
        partes_procesadas = []  # Lista de fragmentos SQL procesados

        operadores = ['=', 'LIKE', '<', '>', '<=', '>=', '!=']  # Operadores soportados

        for i, parte in enumerate(partes):
            if parte[0]:  # Si está entre comillas simples
                valor = parte[0]
                parametros.append(valor)
            elif parte[1]:  # Si está entre comillas dobles
                valor = parte[1]
                parametros.append(valor)
            else:  # Caso de palabra o expresión sin comillas
                valor = parte[2]

                # Verificar si contiene un operador
                for operador in operadores:
                    if operador in valor.upper():
                        columna, valor = map(str.strip, valor.split(operador, 1))
                        partes_procesadas.append(f"{columna} {operador} ?")
                        if valor != '':
                            parametros.append(valor)
                        break
                else:
                    # Si no es un operador, agregarlo como está (e.g., AND, OR)
                    partes_procesadas.append(valor)

        # Reconstruir la cláusula con las partes procesadas
        agregado = ' '.join(partes_procesadas)

        return agregado, parametros
