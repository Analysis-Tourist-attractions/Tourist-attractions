from __init__ import *


def migrate_crawl(sitename):
    sitename = f"CREATE TABLE IF NOT EXISTS {sitename} ("
    for column in crawl_c:
        sitename += (
            f"`{column}` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci, "
        )
    sitename = sitename[:-2] + ")"
    mycursor.execute(sitename)
    mydb.commit()
    mydb.close()


def migrate_visitor():
    visitor_table = f"CREATE TABLE IF NOT EXISTS `Visitor` ("
    for column in visitor_c:
        if column == "Year" or column == "Month":
            visitor_table += f"`{column}` INT, "
        elif column == "Visitor_count" or column == "Visitor_ratio":
            visitor_table += f"`{column}` FLOAT, "
        else:
            visitor_table += f"`{column}` VARCHAR(255), "
    visitor_table = visitor_table[:-2] + ")"
    mycursor.execute(visitor_table)
    mydb.commit()
    mydb.close()


def migrate_expenditure():
    expenditure_table = f"CREATE TABLE IF NOT EXISTS Expenditure ("
    for column in expenditure_c:
        if column == "Year" or column == "Month":
            expenditure_table += f"`{column}` INT, "
        elif column == "Expenditure" or column == "Expenditure_ratio":
            expenditure_table += f"{column} FLOAT, "
        else:
            expenditure_table += f"{column} VARCHAR(255), "
    expenditure_table = expenditure_table[:-2] + ")"
    mycursor.execute(expenditure_table)
    mydb.commit()
    mydb.close()


def migrate_search():
    search_table = f"CREATE TABLE IF NOT EXISTS Search ("
    for column in search_c:
        if column == "Year" or column == "Month":
            search_table += f"`{column}` INT, "
        elif "count" in column:
            search_table += f"{column} FLOAT, "
        else:
            search_table += f"{column} VARCHAR(255), "
    search_table = search_table[:-2] + ")"
    mycursor.execute(search_table)
    mydb.commit()
    mydb.close()


def migrate_distance():
    Distance_table = f"CREATE TABLE IF NOT EXISTS `Distance` ("
    for column in distance_c:
        if column == "Year" or column == "Month":
            Distance_table += f"`{column}` INT, "
        elif column == "Region" or column == "Local_government" or column == "Distance":
            Distance_table += f"`{column}` VARCHAR(255), "
        else:
            Distance_table += f"`{column}` FLOAT, "
    Distance_table = Distance_table[:-2] + ")"
    mycursor.execute(Distance_table)
    mydb.commit()
    mydb.close()
