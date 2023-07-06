import mysql.connector

# clase DAO encargada como capa intermedia entre la aplicacion y la bd,
# llama a las funciones para abrir y cerrar la bd, como tambien el CRUD de los módulos
class DAO:
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='', host='localhost', database='fixedpc')
        self.cursor = self.cnx.cursor()

    def buscar(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def crear(self, query):
        self.cursor.execute(query)
        self.cnx.commit()
        return self.cursor.lastrowid

    def modificar(self, query, values):
        self.cursor.execute(query, values)
        self.cnx.commit()
        return self.cursor.rowcount

    def eliminar(self, query):
        self.cursor.execute(query)
        self.cnx.commit()
        return self.cursor.rowcount

    def mostrar(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def cerrar_conexion(self):
        self.cursor.close()
        self.cnx.close()
