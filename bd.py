import mysql.connector
from mysql.connector import errorcode
import sys
import settings
from datetime import datetime


try:
    db = mysql.connector.connect(
        host=settings.bd_host,
        user=settings.bd_user,
        passwd=settings.bd_passwd,
        database=settings.bd_database
    )

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Try again")
        sys.exit()
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database doesn't exist")
        sys.exit()
    else:
        print(err)
        sys.exit()


cursor = db.cursor()


def get_timetable():
    list_activity_location = list()
    cursor.execute("SELECT data_time, activity, location FROM vyezd_suir.test_timetable")
    now = datetime.now().time()
    for row in cursor.fetchall():
        db_time = row[0].time()
        if now < db_time:
            list_activity_location.append(row[1])
            list_activity_location.append(row[2])
    return list_activity_location


def add_user_id(user_id):
    sql = "INSERT INTO vyezd_suir.users (user_id) VALUES (%s)"
    val = (user_id,)
    cursor.execute(sql, val)
    db.commit()


def get_user_id():
    user_id_list = list()
    cursor.execute("SELECT user_id FROM vyezd_suir.users")
    for row in cursor.fetchall():
        user_id_list.append(int(row[0]))
    return user_id_list


def user_checking(user_id):
    cursor.execute("SELECT * FROM vyezd_suir.users WHERE user_id=%s",
                   (user_id,))
    result = cursor.fetchone()
    return result is not None


def add_user_name(name, user_id):
    sql = "INSERT INTO vyezd_suir.users (name) VALUES (%s) WHERE user_id=%s"
    val = (name, user_id)
    cursor.execute(sql, val)
    db.commit()


def add_info(user_id, name, surname, isu_number):
    sql = "UPDATE vyezd_suir.users SET name = %s, surname = %s, isu_number = %s WHERE user_id = %s"
    val = (name.capitalize(), surname.capitalize(), isu_number, user_id)
    cursor.execute(sql, val)
    db.commit()
