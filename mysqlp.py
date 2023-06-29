import pymysql
import time
import datetime


def connect():
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M:%S')
    vehicle_name = 'Honda CR-V'
    price = 12000000
    description = 'Всякая ерунда'
    manufacture_year = '2013'
    body = 'Кроссовер'
    engine = '2,4'
    wheel = 'Левый руль'
    transmission = 'КПП автомат'
    city = 'Алматы'
    date_add = '12 июня'
    views = 1236
    uniq_id = 'https://photos-kl.kcdn.kz/webp/51/51f2b1d7-8ff0-4ac8-8021-99621968412b/1-200x150.webp'
    url = 'https://kolesa.kz'
    try:
        connection = pymysql.connect(
            host='52.28.161.82',
            port=3306,
            user='stick',
            password='Cbybq123_',
            database='kolesa_db',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                # create_table_query = "CREATE TABLE adds(id int AUTO_INCREMENT, " \
                #                      "date_load timestamp, " \
                #                      "name varchar(64), " \
                #                      "price int, " \
                #                      "description text, " \
                #                      "city varchar(64), " \
                #                      "date_add varchar(32), " \
                #                      "views int, " \
                #                      "manufacture_year varchar(32), " \
                #                      "body varchar(64), " \
                #                      "engine varchar(64), " \
                #                      "wheel varchar(64), " \
                #                      "transmission varchar(64), " \
                #                      "uniq_id varchar(256), " \
                #                      "url varchar(256), " \
                #                      "PRIMARY KEY (id));"
                # cursor.execute(create_table_query)
                # cursor.execute("""INSERT INTO adds (date_load, name, price, description, city, date_add, views, manufacture_year, body, engine, wheel, transmission, uniq_id, url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (timestamp, vehicle_name, price, description, city, date_add, views, manufacture_year, body, engine, wheel, transmission, uniq_id, url))
                # delete_table_query = "DROP TABLE adds;"


                # alter_table_query = "ALTER TABLE adds MODIFY COLUMN date_load varchar(32);"
                # alter_table_query = "ALTER TABLE adds ADD fuel VARCHAR(32);"
                # cursor.execute(alter_table_query)

                delete_query = "DELETE FROM adds;"
                cursor.execute(delete_query)

                connection.commit()
                print("table modified")
        finally:
            connection.close()
    except Exception as ex:
        print(ex)


def main():
    connect()


if __name__ == '__main__':
    main()
