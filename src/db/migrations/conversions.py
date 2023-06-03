import utils
from __init__ import *

mydb = utils.get_mysql_connection(host, user, password, database)
mycursor = mydb.cursor()


def mysql_to_csv(table):
    mycursor.execute(f"SELECT * FROM {table}")
    result = mycursor.fetchall()

    with open(f"{table}.csv", mode="w", encoding="cp949", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([i[0] for i in mycursor.description])
        writer.writerows(result)
