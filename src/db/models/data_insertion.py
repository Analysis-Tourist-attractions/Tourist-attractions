from __init__ import *
from utils import *


def insert_crawl(sitename):
    for filename in sorted(os.listdir(f"src/db/크롤링-데이터/{sitename}")):
        file_path = os.path.join(f"src/db/크롤링-데이터/{sitename}", filename)
        file_path = file_path.replace("\\", "/")

        # 파일명에서 Local 추출
        _, Local = filename[:-4].split("_")
        col = sitename + "_c"

        # 파일 읽기 & DB에 데이터 삽입
        with open(file_path, encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                content = row[0][:500]
                insert_row_sql = "INSERT INTO {} (`{}`, `{}`) VALUES (%s, %s)".format(
                    sitename, col[0], col[1]
                )
                values = (Local, content)
                mycursor.execute(insert_row_sql, values)

    mydb.commit()
    mydb.close()


def insert_visitor():
    for filename in sorted(
        os.listdir("src/db/월별데이터/월별방문자수"),
        key=lambda x: int(x.split("_")[2].replace("월", "")),
    ):
        file_path = os.path.join("src/db/월별데이터/월별방문자수", filename)
        file_path = file_path.replace("\\", "/")

        # 파일명에서 지역, 기초지자체명, year, month를 추출
        _, year_str, month_str, region, *_ = filename[:-4].split("_")
        month = int(month_str.replace("월", ""))
        year = int(year_str)

        # 파일 읽기 & DB에 데이터 삽입
        with open(file_path, encoding="cp949") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                insert_row_sql = f"INSERT INTO `Visitor` (`{visitor_c[0]}`, `{visitor_c[1]}`, `{visitor_c[2]}`, `{visitor_c[3]}`, `{visitor_c[4]}`, `{visitor_c[5]}`) VALUES ('{region}', '{row[0]}', {int(year)}, {int(month)}, {row[1]}, {row[2]})"
                mycursor.execute(insert_row_sql)

    mydb.commit()
    mydb.close()


def insert_expenditure():
    for filename in sorted(
        os.listdir("src/db/월별데이터/월별지역별지출"),
        key=lambda x: int(x.split("_")[2].replace("월", "")),
    ):
        file_path = os.path.join("src/db/월별데이터/월별지역별지출", filename)
        file_path = file_path.replace("\\", "/")

        # 파일명에서 year, month, 지역, 기초지자체명을 추출.
        _, year_str, month_str, region, _, *_ = filename[:-4].split("_")
        month = int(month_str.replace("월", ""))
        year = int(year_str)

        # 파일 읽기 & DB에 데이터 삽입
        with open(file_path, encoding="cp949") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                insert_row_sql = f"INSERT INTO `Expenditure` (`{expenditure_c[0]}`, `{expenditure_c[1]}`, `{expenditure_c[2]}`, `{expenditure_c[3]}`, `{expenditure_c[4]}`, `{expenditure_c[5]}`) VALUES ('{region}', '{row[0]}', {int(year)}, {int(month)}, {row[1]}, {row[2]})"
                mycursor.execute(insert_row_sql)

    mydb.commit()
    mydb.close()


def insert_search():
    for filename in sorted(
        os.listdir("src/db/월별데이터/월별네비게이션검색건수"),
        key=lambda x: int(x.split("_")[2].replace("월", "")),
    ):
        file_path = os.path.join("src/db/월별데이터/월별네비게이션검색건수", filename)
        file_path = file_path.replace("\\", "/")

        # 파일명에서 지역, 기초지자체명, year, month를 추출
        _, year_str, month_str, region, _, *_ = filename[:-4].split("_")
        month = int(month_str.replace("월", ""))

        # year 값을 2자리에서 4자리로 변환
        if len(year_str) == 2:
            year_str = "20" + year_str
        year = int(year_str)

        # 파일 읽기 & DB에 데이터 삽입
        with open(file_path, encoding="cp949") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                insert_row_sql = f"INSERT INTO `Search` (`{search_c[0]}`, `{search_c[1]}`, `{search_c[2]}`, `{search_c[3]}`, `{search_c[4]}`, `{search_c[5]}`, `{search_c[6]}`, `{search_c[7]}`, `{search_c[8]}`) VALUES ('{region}', '{row[0]}', '{row[1].strip()}', {year}, {month}, {float(row[2])}, {float(row[3])}, {float(row[4])}, {float(row[5].strip())})"
                mycursor.execute(insert_row_sql)

    mydb.commit()
    mydb.close()


def insert_distance():
    for filename in sorted(
        os.listdir("src/db/월별데이터/거리"),
        key=lambda x: int(x[:-4].split("_")[4]),
    ):
        file_path = os.path.join("src/db/월별데이터/거리", filename)
        file_path = file_path.replace("\\", "/")

        # 파일명에서 Region, Local_government, year, month를 추출
        _, Region, Local_government, year_str, month_str = filename[:-4].split("_")
        year = int(year_str)
        month = int(month_str)

        # 파일 읽기 & DB에 데이터 삽입
        with open(file_path, encoding="cp949") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                distance = row[0].replace("이상", "over").replace("미만", "under")
                insert_row_sql = f"INSERT INTO `Distance` (`{distance_c[0]}`, `{distance_c[1]}`, `{distance_c[2]}`, `{distance_c[3]}`, `{distance_c[4]}`, `{distance_c[5]}`, `{distance_c[6]}`) VALUES ('{Region}', '{Local_government}', {year}, {month}, '{distance}', {row[1]}, {row[2]})"
                mycursor.execute(insert_row_sql)

    mydb.commit()
    mydb.close()
