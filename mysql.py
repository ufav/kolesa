import pymysql
from hashlib import sha256


try:
    connection = pymysql.connect(
        host='52.28.161.82',
        port=3306,
        user='stick',
        password="Cbybq123_",
        database='kolesa_db',
        cursorclass=pymysql.cursors.DictCursor
    )
    print('Успешно')
    print('#' * 20)

except Exception as ex:
    print('Неуспешно')
    print(ex)