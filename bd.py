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
    sql = "INSERT IGNORE INTO vyezd_suir.users (user_id) VALUES (%s)"
    val = (user_id,)
    cursor.execute(sql, val)
    db.commit()

