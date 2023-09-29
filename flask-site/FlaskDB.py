import sqlite3
import math
import time
from flask import url_for

class FlaskDB:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    
    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []
    
    
    def addUser(self, name, contact, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False
 
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?)", (name, email, hpsw, tm, contact))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД "+str(e))
            return False
 
        return True
    
    def activateUser(self, id):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM rent WHERE uid = '{id}' AND carid = 5 AND days = 1000")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь активен")
                return False
 
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO rent VALUES(?, ?, ?)", (5, id, 1000))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД "+str(e))
            return False
 
        return True

    
    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE uid = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False 
 
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
 
        return False
    
    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД"+str(e))

        return False
        
    def getCarOnce(self):
        try:
            self.__cur.execute(f"SELECT carid, carname, platenumber, power, picture,\
                                price, status\
                                FROM cars ORDER BY carid")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения из БД"+str(e))
            return False
        
        return[]

    def getCar(self, alias):
        try:
            self.__cur.execute(f"SELECT carid, carname, platenumber, power, picture,\
                                price, status\
                                FROM cars WHERE carid LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения из БД"+str(e))
            return False
        
        return[]

    def takeCar(self, alias, uid, days):
        try:
            self.__cur.execute("INSERT INTO rent VALUES(?, ?, ?)", (alias, uid, days))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Не получилось взять данные о машине из БД"+str(e))
            return False
        return True
    
    def userCars(self, id):
        try:
            self.__cur.execute(f"SELECT cars.carname, rent.days\
                                    FROM rent, cars\
                                    WHERE rent.uid = '{id}' AND cars.carid=rent.carid")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения книги из БД"+str(e))

    def switchCar(self, carid):
        try:
            self.__cur.execute("UPDATE cars SET status = ? WHERE carid = ?", (0, carid))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка получения данных о машине из БД"+str(e))
            return False
        return True

    def feedBack(self, title, text, msg):
        try:
            self.__cur.execute("INSERT INTO contact VALUES( ?, ?, ?)", (title, text, msg))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД "+str(e))
            return False
 
        return True