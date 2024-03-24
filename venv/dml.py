import pymysql


class DML:
    result = []
    __host = "localhost"
    __user = "root"
    __db = "xyz"
    __port = 3306

    def __init__(self, host, user, db, port):
        self.__host = host
        self.__user = user
        self.__db = db
        self.__port = port

    def conectar(self):
        self.db = pymysql.connect(
            host=self.__host,
            user=self.__user,
            db=self.__db,
            port=self.__port)
        cur = self.db.cursor()
        self.cursor = cur

    # def consultar(self, query):
    #     self.cursor.execute(query)
    #     # self.result = self.cursor.fetchall()
    #     for info in self.cursor.fetchall():
    #         self.result.append(info)
    #
    #     self.imprimir()

    def insertar(self, query):
        self.cursor.execute(query)
        self.db.commit()

    #
    # def actualizar(self, query):
    #     self.cursor.execute(query)
    #     self.db.commit()
    #
    # def eliminar(self, query):
    #     self.cursor.execute(query)
    #     self.db.commit()
    #
    # def imprimir(self):
    #     for filas in self.result:
    #         print(filas)

    def cerrar_conex(self):
        self.db.close()

