from classes import User, Pari, User_list, Pari_list
from db import get_pari, update_user_db, update_pari_db, open_db, add_user_db
import db
import sqlite3

DATABASE_URL = 'db.sqlite'
user_1 = User('Vasya','0000_0000_0000_0001')

# add_user_db(DATABASE_URL, user_1)
#
# conn = sqlite3.connect('db.sqlite')
#
# # cursor - позволяет выполнять запросы
# cursor = conn.cursor()
#
#
# cursor.execute('SELECT name FROM users')
# result = cursor.fetchmany(size=10)
#
# print(result)
# print(type(result))
#
#
# conn.close()
#
l = {'a':1, 'b':2}
l.get('a')
for numb in l.keys():
    print(l.get(numb))




