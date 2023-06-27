import pymysql


def connect():
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
                #                      "date_add date, " \
                #                      "vehicle_name varchar(64), " \
                #                      "price int, " \
                #                      "description text, " \
                #                      "region varchar(64), " \
                #                      "city varchar(64), " \
                #                      "views int, " \
                #                      "PRIMARY KEY (id));"
                # cursor.execute(create_table_query)
                insert_data_query = "INSERT INTO adds (date_load, date_add, vehicle_name, price, description, region, " \
                                    "city, views) VALUES (now(), now(), 'Honda CR-V', '12000000', 'sdfsdfsdgdfgdfggsdg', " \
                                    "'Алматы', 'Алматы', '579'); "
                cursor.execute(insert_data_query)
                connection.commit()
                print("Data inserted")
        finally:
            connection.close()
    except Exception as ex:
        print(ex)


def main():
    connect()


if __name__ == '__main__':
    main()

